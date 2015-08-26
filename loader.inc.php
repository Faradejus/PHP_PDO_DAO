<?php

    require_once("./Common/statement.class.php");
    require_once("./Common/DB.class.php");


    function load_newDB(){
        return new DB("localhost", "USER", "PASS", "DB");
    }