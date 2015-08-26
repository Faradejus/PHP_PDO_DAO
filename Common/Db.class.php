<?php
    require("Log.class.php");

    class DB
    {
        private $host;
        private $user;
        private $password;
        private $database;

        private $pdo;
        private $sQuery;
        private $bConnected = false;
        private $log;
        private $parameters;
        public  $dbErros = null;

        public function getDbErrors(){
            return $this->dbErros;
        }

        public function __construct($host=null, $user=null, $password=null, $database=null) {
            $this->host = $host;
            $this->user = $user;
            $this->password = $password;
            $this->database = $database;

            $this->log = new Log();
            $this->Connect();
            $this->parameters = array();
            $this->dbErros = null;
        }

        private function Connect() {
            $dsn = 'mysql:dbname='.$this->database.';host='.$this->host;
            try {
                $this->pdo = new PDO($dsn, $this->user, $this->password, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
                $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                $this->pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
                $this->bConnected = true;
            }
            catch (PDOException $e) {
                $this->ExceptionLog($e->getMessage());
                exit("Nepavyko prisijunkti prie duomenų bazės!");

            }
        }


        public function CloseConnection() {
            var_dump("CLOSE CONNECTION");
            $this->pdo = null;
        }

        private function Init($query,$parameters = "") {
            if(!$this->bConnected)
                $this->Connect();

            try {
                $this->sQuery = $this->pdo->prepare($query);
                $this->bindMore($parameters);

                if(!empty($this->parameters)) {
                    foreach($this->parameters as $param)
                    {
                        $parameters = explode("\x7F",$param);
                        $this->sQuery->bindParam($parameters[0],$parameters[1]);
                    }
                }

                $this->succes 	= $this->sQuery->execute();
            }
            catch(PDOException $e)
            {
                $this->ExceptionLog($e->getMessage(), $query );
                return false;
            }

            $this->parameters = array();
            return true;
        }


        public function bind($para, $value) {
            $this->parameters[sizeof($this->parameters)] = ":" . $para . "\x7F" . utf8_encode($value);
        }

        public function bindMore($parray) {
            if(empty($this->parameters) && is_array($parray)) {
                $columns = array_keys($parray);
                foreach($columns as $i => &$column)	{
                    $this->bind($column, $parray[$column]);
                }
            }
        }

        public function query($query,$params = null, $fetchmode = PDO::FETCH_ASSOC)
        {
            $query = trim($query);

            if (!$this->Init($query,$params)){
                return null;
            }

            $rawStatement = explode(" ", $query);

            $statement = strtolower($rawStatement[0]);

            if ($statement === 'select' || $statement === 'show') {
                return $this->sQuery->fetchAll($fetchmode);
            }
            elseif ( $statement === 'insert' ||  $statement === 'update' || $statement === 'delete' ) {
                return $this->sQuery->rowCount();
            }
            else {
                return NULL;
            }
        }


        public function lastInsertId() {
            return $this->pdo->lastInsertId();
        }

        public function column($query,$params = null) {
            $this->Init($query,$params);
            $Columns = $this->sQuery->fetchAll(PDO::FETCH_NUM);

            $column = null;

            foreach($Columns as $cells) {
                $column[] = $cells[0];
            }

            return $column;

        }

        public function row($query,$params = null,$fetchmode = PDO::FETCH_ASSOC) {
            if(!$this->Init($query,$params))
                return null;

            return $this->sQuery->fetch($fetchmode);
        }

        public function single($query,$params = null) {
            $this->Init($query,$params);
            return $this->sQuery->fetchColumn();
        }

        private function ExceptionLog($message , $sql = "") {
            $message;

            if(!empty($sql)) {
                $message .= "\r\nRaw SQL : "  . $sql;
            }

            //TODO pakeisti i konstantas
            $this->dbErros = $message;

            $this->log->write($message);
        }

        function getFQFieldName($field, $table){
            return $table.".".$field;
        }

        function getQFieldName($field){
            return $field;
        }

        function toBoolean($value) {
            if (is_null( $value )) {
                return NULL;
            } else if ($value) {
                return TRUE;
            } else {
                return FALSE;
            }
        }

        public function beginTran(){
            try {
                return $this->pdo->beginTransaction();
            }
            catch (PDOException $e) {
                $this->ExceptionLog($e->getMessage());
                return $this->getDbErrors();
            }
        }

        public function commitTran(){
            try {
                return $this->pdo->commit();
            }
            catch (PDOException $e) {
                $this->ExceptionLog($e->getMessage());
                return $this->getDbErrors();
            }

        }

        public function rollTran(){
            try {
                return $this->pdo->rollBack();
            }
            catch (PDOException $e) {
                $this->ExceptionLog($e->getMessage());
                return $this->getDbErrors();
            }
        }
    }
?>
