<?php

class AbstractStatement {

	function setStatements($statements){
		return;
	}

	function getStatements(){
		return;
	}

	function toString(){
		return;
	}

    function prepareWhereStatement($field,$operator="="){
        return $field." ". $operator ." :".$field;
    }
} 

class AndStatement extends AbstractStatement {

	var $statements;
    var $values = array();

	function AndStatement($field=null, $value=null, $operator="="){
        if (!is_null($field)){
            $this->setParams($field,$value);
            $field = $this->prepareWhereStatement($field,$operator);
        }

		$this->statements = $field;
	}

	function setStatements($statements){
		$this->statements = $statements;
	}

	function getStatements(){
		return $this->statements;
	}

    function addStatement($field, $value=null, $operator="="){
        if(!is_object($field)){
            $this->setParams($field,$value);
            $field = $this->prepareWhereStatement($field,$operator);
        }

        if (is_null($this->statements)){
            $this->statements = array($field);
        } else if (is_string($this->statements)){
            $this->statements = array($this->statements, $field);
        } else if (is_array($this->statements)){
            array_push($this->statements, $field);
        }
        return $this;
    }

	function toString(){
		$result = "";
		$sep = "";
		if (is_string($this->statements)){
			$result = $this->statements;
		} else if (is_array($this->statements)){
			foreach ($this->statements as $statement) {
				if (is_string($statement)){
					$result .= $sep.$statement;
					$sep = " AND ";
				} else if (is_object($statement)){
					$complexStatement = $statement;
					$result .= $sep."(".$complexStatement->toString().")";
					$sep = " AND ";

                    $params = $complexStatement->getParams();
                    foreach($params as $name=>$value){
                        $this->setParams($name,$value);
                    }
				}				
			}
		}
		if (strlen($result) <= 0){
			$result = "1=1";
		}
		return $result;
	}

    function getParams(){
        return $this->values;
    }

    function setParams($field,$value){
        if(!isset($this->values[$field])){
            $this->values[$field] = $value;
        }
    }
} 

class OrStatement extends AbstractStatement {

	var $statements;
    var $values;

	function OrStatement($field=null, $value=null, $operator="=") {
        if (!is_null($field)){
            $this->setParams($field,$value);
            $field = $this->prepareWhereStatement($field,$operator);
        }

        $this->statements = $field;
    }

	function setStatements($statements){
		$this->statements = $statements;
	}

	function getStatements(){
		return $this->statements;
	}

	function addStatement($field, $value=null, $operator="="){
        if(!is_object($field)){
            $this->setParams($field,$value);
            $field = $this->prepareWhereStatement($field,$operator);
        }

        if (is_null($this->statements)){
            $this->statements = array($field);
        } else if (is_string($this->statements)){
            $this->statements = array($this->statements, $field);
        } else if (is_array($this->statements)){
            array_push($this->statements, $field);
        }
        return $this;
	}

	function toString(){
		$result = "";
		$sep = "";
		if (is_string($this->statements)){
			$result = $this->statements;
		} else if (is_array($this->statements)){
			foreach ($this->statements as $statement) {
				if (is_string($statement)){
					$result .= $sep.$statement;
					$sep = " OR ";
				} else if (is_object($statement)){
					$complexStatement = $statement;
					$result .= $sep."(".$complexStatement->toString().")";
					$sep = " OR ";

                    $params = $complexStatement->getParams();
                    foreach($params as $name=>$value){
                        $this->setParams($name,$value);
                    }
				}				
			}
		}
		if (strlen($result) <= 0){
			$result = "1=0";
		}
		return $result;
	}

    function getParams(){
        return $this->values;
    }

    function setParams($field,$value){
        if(!isset($this->values[$field])){
            $this->values[$field] = $value;
        }
    }
}

class OrderBy {

	var $fieldName;
	var $ascending;

	function OrderBy($fieldName=null, $ascending=true){
		$this->fieldName = $fieldName;
		$this->setAscending($ascending);
	}

	function setFieldName($fieldName){
		$this->fieldName = $fieldName;
	}

	function getFieldName(){
		return $this->fieldName;
	}

	function setAscending($ascending){
		if ($ascending){
			$this->ascending = true;
		} else {
			$this->ascending = false;
		}
	}

	function isAscending(){
		return $this->asc;
	}

	function toString(){
		$result = "";
		if (strlen($this->fieldName) > 0){
			if ($this->ascending){
				$result = $this->fieldName." ASC";
			} else {
				$result = $this->fieldName." DESC";
			}			
		}
		return $result;
	}

}

class OrderBys {

	var $orders;

	function OrderBys($orderBy=null){
		if (is_object($orderBy)){
			$this->orders = array($orderBy);
		} else {
			$this->orders = array();
		}
	}

	function addField($fieldName, $ascending=true){
		$orderBy = new OrderBy($fieldName, $ascending);
		return $this->addOrderBy($orderBy);
	}
	
	function addFieldFirst($fieldName, $ascending=true){
		$orderBy = new OrderBy($fieldName, $ascending);
		return $this->addOrderByFirst($orderBy);
	}

	function addOrderBy($orderBy){
		array_push($this->orders, $orderBy);
		return $this;
	}
	
	function addOrderByFirst($orderBy){
		$fieldName = "";
		if (is_string($orderBy)){
			$fieldName = $orderBy;
		} else if (is_object($orderBy)){
			$fieldName = $orderBy->getFieldName();
		}
		$orders2 = array();
		foreach ($this->orders as $ord){
			$remove = false;
			if (is_string($ord)){
				$remove = $ord == $fieldName;
			} else if (is_object($ord)){
				$remove = $ord->getFieldName() == $fieldName;
			}
			if (!$remove){
				array_push($orders2, $ord);
			}
		}
		$this->orders = $orders2;
		array_unshift($this->orders, $orderBy);
		return $this;
	}

	function toString(){
		$result = "";
		$sep = "ORDER BY ";
		foreach ($this->orders as $order) {
			$orderStr = $order->toString();
			if (strlen($orderStr) > 0){
				$result = $result.$sep.$orderStr;
				$sep = ", ";
			}
		}
		return $result;
	}
	
	function size(){
		return count($this->orders);
	}
}

class InStatement {

	var $field;
	var $values;
	var $not;
	
	function InStatement($field=null, $values=null, $not=false){
		$this->field = $field;
		$this->values = $values;
		$this->not = $not;
	}

	function setField($field){
		$this->field = $field;
	}

	function getField(){
		return $this->field;
	}

	function setValues($values){
		$this->values = $values;
	}

	function getValues(){
		return $this->values;
	}

	function setNot($not){
		$this->not = $not;
	}

	function isNot(){
		return $this->not;
	}

	function addValue($value){
		if (is_array($this->values)){
			//array_push($this->values, $value);
			$this->values[serialize($value)] = $value;
		} else {
			//$this->values = array($value);
			$this->values = array(serialize($value)=>$value);
		}
		return $this;
	}

	function toString(){
		$sNot = "";
		if ($this->not) {
			$sNot = "NOT ";
		}
		if (!is_array($this->values)){
			return $sNot."1=0";
		} else if (!is_string($this->field)){
			return $sNot."1=0";
		} else if (count($this->values) <= 0){
			return $sNot."1=0";
		}
		$result = "";
		$sep = "";
		foreach ($this->values as $value){
			if (is_bool($value)){
				if ($value){
					$result .= $sep."true";
				} else {
					$result .= $sep."false";
				}
			} else {
				$result .= $sep."'".addslashes($value)."'";
			}
			$sep = ", ";
		}
		if (strlen($result) <= 0){
			return $sNot."1=0";
		}
		$result = $this->field." ".$sNot."IN (".$result.")";
		return $result;
	}
}

?>