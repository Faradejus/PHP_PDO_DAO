#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HEADER
def generateBean(table, pks, fields):
    sp = "    "
    className = table[1][0:1].capitalize() + table[1][1:]
    result = "class " + className + " {\n\n"
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    for field in allFields:
        nice = field[1]
        result += sp + "var $" + nice + ";\n"
    result += "\n" + sp + "function " + className + "("
    sep = ""
    for field in allFields:
        nice = field[1]
        result += sep + "$" + nice + "=null"
        sep = ", "
    result += "){\n"
    for field in allFields:
        nice = field[1]
        result += sp + sp + "$this->" + nice + " = $" + nice + ";\n"
    result += sp + "}\n"
    for field in allFields:
        nice = field[1]
        setter = "set" + nice[0:1].capitalize() + nice[1:]
        if field[2] == "boolean":
            getter = "is" + nice[0:1].capitalize() + nice[1:]
        else:
            getter = "get" + nice[0:1].capitalize() + nice[1:]
        result += "\n" + sp + "function " + setter + "($" + nice + "){\n"
        result += sp + sp + "$this->" + nice + " = $" + nice + ";\n"
        result += sp + "}\n"
        result += "\n" + sp + "function " + getter + "(){\n"
        result += sp + sp + "return $this->" + nice + ";\n"
        result += sp + "}\n"
    result += "}\n"
    return result

#GET
def generateGet(table, pks, fields):
    sp = "    "
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    result = "\n" + sp + "function buildGetQuery(){\n"
    sep = ""
    #for field in pks:
    #    nice = field[1]
    #    result += sep + "$" + nice
    #    sep = ", "
    #result += "){\n"
    result += sp + sp + "$result = \"SELECT\";\n"
    sep = "\" \""
    for field in allFields:
        nice = field[1]
        getter = "getFQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += sp + sp + "$result .= " + sep + ".$this->" + getter + "();\n";
        sep = "\", \""
    result += sp + sp + "$result .= \" FROM \".$this->tableName;\n"
    sep = "\" WHERE \""
    for field in pks:
        nice = field[1]
        getter = "getFQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        getterName = "get" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += sp + sp + "$result .= " + sep + ".$this->" + getter + "();\n"
        result += sp + sp + "$result .= \" = :\" . $this->" + getterName + "();\n"
        sep = "\" AND \""
    result += sp + sp + "$result .= \" LIMIT 1\";\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function get("
    sep = ""
    for field in pks:
        nice = field[1]
        result += sep + "$" + nice
        sep = ", "
    result += "){\n"
    result += sp + sp + "$query = $this->buildGetQuery();\n\n"
    result += sp + sp + "$params = array(\n"
    sep = ""
    for field in pks:
        nice = field[1]
        getterName = "get" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += sp + sp + sp + sep + "$this->" + getterName + "() => $" + nice + "\n"
        sep = ", "
    result += sp + sp + ");\n\n"
    result += sp + sp + "$result = $this->database->row($query, $params, PDO::FETCH_NUM);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors()))\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n\n"
    result += sp + sp + "if (is_null($result))\n"
    result += sp + sp + sp + "return $result;\n\n";
    objectName = table[1][0:1].lower() + table[1][1:]
    result += sp + sp + "$" + objectName + " = null;\n"
    result += sp + sp + "if ($result){\n"
    className = table[1][0:1].capitalize() + table[1][1:]
    result += sp + sp + sp + "$" + objectName + " = new " + className + "();\n"
    indx = 0
    for field in allFields:
        nice = field[1]
        setter = "set" + nice[0:1].capitalize() + nice[1:]
        result += sp + sp + sp + "$value = $result[" + str(indx) + "];\n"
        if field[2] == "boolean":
            result += sp + sp + sp;
            result += "$value = $this->database->toBoolean($value);\n"
        result += sp + sp + sp + "$" + objectName + "->" + setter
        result += "($value);\n";
        indx += 1
    result += sp + sp + "}\n"
    result += sp + sp + "return $" + objectName + ";\n"
    result += sp + "}\n"
    return result

#FIND
def generateFind(table, pks, fields):
    sp = "    "
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    result = "\n" + sp + "function buildFindQuery("
    result += "$criteria=null, $order=null, $limit=1000, $from=0){\n"
    result += sp + sp + "$result = \"SELECT\";\n"
    sep = "\" \""
    for field in allFields:
        ftype = field[2]
        if ftype != "text" and ftype != "binary":
            nice = field[1]
            getter = "getFQ" + nice[0:1].capitalize() + nice[1:] + "Name"
            result += sp + sp + "$result .= " + sep
            result += ".$this->" + getter + "();\n"
            sep = "\", \""
    result += sp + sp + "$result .= \" FROM \".$this->tableName;\n"
    result += sp + sp + "if (!is_null($criteria)){\n"
    result += sp + sp + sp + "$result .= \" WHERE \".$criteria->toString();\n"
    result += sp + sp + "}\n"
    result += sp + sp + "if (!is_null($order)){\n"
    result += sp + sp + sp + "$result .= \" \".$order->toString();\n"
    result += sp + sp + "}\n"
    result += sp + sp + "$result .= \" LIMIT \".$limit.\" OFFSET \".$from;\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function find("
    result += "$criteria=null, $order=null, $limit=1000, $from=0){\n"
    result += sp + sp + "$query = $this->buildFindQuery($criteria, $order, $limit, $from);\n\n"
    result += sp + sp + "$params = null;\n"
    result += sp + sp + "if(!is_null($criteria))\n"
    result += sp + sp + sp + "$params = $criteria->getParams();\n\n"
    result += sp + sp + "$result = $this->database->query($query, $params, PDO::FETCH_NUM);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors()))\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n\n"
    result += sp + sp + "if (is_null($result))\n"
    result += sp + sp + sp + "return $result;\n\n"
    objectName = table[1][0:1].lower() + table[1][1:]
    result += sp + sp + "$" + objectName + "s = array();\n"
    result += sp + sp + "foreach($result as $row){\n"
    className = table[1][0:1].capitalize() + table[1][1:]
    result += sp + sp + sp + "$" + objectName + " = new " + className + "();\n"
    indx = 0
    for field in allFields:
        nice = field[1]
        ftype = field[2]
        if ftype != "text" and ftype != "binary":
            setter = "set" + nice[0:1].capitalize() + nice[1:]
            result += sp + sp + sp + "$value = $row[" + str(indx) + "];\n"
            if field[2] == "boolean":
                result += sp + sp + sp;
                result += "$value = $this->database->toBoolean($value);\n"
            result += sp + sp + sp + "$" + objectName + "->" + setter
            result += "($value);\n";
            indx += 1
    indx = ""
    sep = ""
    for field in pks:
        nice = field[1]
        if field[2] == "boolean":
            getter = "is" + nice[0:1].capitalize() + nice[1:]
        else:
            getter = "get" + nice[0:1].capitalize() + nice[1:]
        indx += sep + "$" + objectName + "->" + getter + "()"
        sep = ".\";\"."
    if len(indx) > 0:
        result += sp + sp + sp + "if ($order != null){\n"
        result += sp + sp + sp + sp + "array_push($" + objectName + "s"
        result += ", $" + objectName + ");\n"
        result += sp + sp + sp + "} else {\n"
        result += sp + sp + sp + sp + "$" + objectName + "s[" + indx + "]"
        result += " = $" + objectName + ";\n"
        result += sp + sp + sp + "}\n"
    else:
        result += sp + sp + sp + "array_push($" + objectName + "s"
        result += ", $" + objectName + ");\n"
    result += sp + sp + "}\n"
    result += sp + sp + "return $" + objectName + "s;\n"
    result += sp + "}\n"
    return result

#INSERT
def generateInsert(table, pks, fields):
    sp = "    "
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    objectName = table[1][0:1].lower() + table[1][1:]
    result = "\n" + sp + "function buildInsertQuery("
    result += "$" + objectName + ", $masked=false){\n"
    result += sp + sp + "$fields = \"\";\n"
    result += sp + sp + "$sep = \"\";\n"
    result += sp + sp + "$values = \"\";\n"
    for field in allFields:
        nice = field[1]
        getter = "getQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        if field[2] == "boolean":
            objGet = "is" + nice[0:1].capitalize() + nice[1:] + "()"
        else:
            objGet = "get" + nice[0:1].capitalize() + nice[1:] + "()"
        result += sp + sp + "$field = $this->" + getter + "();\n"
        result += sp + sp + "$value = $" + objectName + "->" + objGet + ";\n"
        result += sp + sp + "$valueP = \":\".$field;\n"
        result += sp + sp + "if (!is_null($value)){\n"
        result += sp + sp + sp + "$fields .= $sep.$field;\n"
        result += sp + sp + sp
        result += "$values .= $sep.\"\".addslashes($valueP).\"\";\n"
        result += sp + sp + sp + "$sep = \", \";\n"
        result += sp + sp + "} else if (!$masked){\n"
        result += sp + sp + sp + "$fields .= $sep.$field;\n"
        result += sp + sp + sp + "$values .= $sep.\"NULL\";\n"
        result += sp + sp + sp + "$sep = \", \";\n"
        result += sp + sp + "};\n"
    result += sp + sp + "$result = \"INSERT INTO \".$this->tableName"
    result += ".\" (\".$fields.\") VALUES (\".$values.\")\";\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function insert("
    result += "&$" + objectName + ", $masked=false){\n"
    result += sp + sp + "$query = $this->buildInsertQuery($"+ objectName +",$masked);\n\n"
    result += sp + sp + "$params = null;\n"
    result += sp + sp + "foreach($"+ objectName +" as $key=>$value){\n"
    result += sp + sp + sp + "if(!is_null($value)){\n"
    result += sp + sp + sp + sp + "$params[strtoupper($key)] = $value;\n"
    result += sp + sp + sp + "}\n"
    result += sp + sp + "}\n\n"
    result += sp + sp + "$result = $this->database->query($query,$params);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors())) {\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n"
    result += sp + sp + "}\n\n"
    if len(pks) >= 1:
        nice = pks[0][1]
        setter = "set" + nice[0:1].capitalize() + nice[1:]
        if pks[0][2] == "boolean":
            objGet = "is" + nice[0:1].capitalize() + nice[1:] + "()"
        else:
            objGet = "get" + nice[0:1].capitalize() + nice[1:] + "()"
        result += sp + sp + "$value = $" + objectName + "->" + objGet + ";\n"
        result += sp + sp + "$newValue = $this->database->lastInsertId();\n"
        if pks[0][2] == "boolean":
            result += sp + sp
            result += "$newValue = $this->database->toBoolean($newValue);\n"
        result += sp + sp + "if (is_null($value)) {\n"
        result += sp + sp + sp
        result += "$" + objectName + "->" + setter + "($newValue);\n"
        result += sp + sp + "}\n\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    return result

#UPDATE
def generateUpdate(table, pks, fields):
    sp = "    "
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    objectName = table[1][0:1].lower() + table[1][1:]
    result = "\n" + sp + "function buildUpdateQuery("
    result += "$" + objectName + ", $masked=false){\n"
    result += sp + sp + "$result = \"UPDATE \".$this->tableName;\n"
    result += sp + sp + "$sep = \" SET \";\n"
    if len(allFields) >= 1:
        nice = allFields[0][1]
        getter = "getQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += sp + sp + "$field = $this->" + getter + "();\n"
        result += sp + sp + "$result .= $sep.$field;\n"
        result += sp + sp + "$result .= \" = \".$field;\n"
        result += sp + sp + "$sep = \", \";\n"
    for field in fields:
        nice = field[1]
        getter = "getQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        if field[2] == "boolean":
            objGet = "is" + nice[0:1].capitalize() + nice[1:] + "()"
        else:
            objGet = "get" + nice[0:1].capitalize() + nice[1:] + "()"
        result += sp + sp + "$field = $this->" + getter + "();\n"
        result += sp + sp + "$value = $" + objectName + "->" + objGet + ";\n"
        result += sp + sp + "$valueP = \":\".$field;\n"
        result += sp + sp + "if (!is_null($value)){\n"
        result += sp + sp + sp + "$result .= $sep.$field;\n"
        result += sp + sp + sp
        result += "$result .= \" = \".addslashes($valueP).\"\";\n"
        result += sp + sp + sp + "$sep = \", \";\n"
        result += sp + sp + "} else if (!$masked){\n"
        result += sp + sp + sp + "$result .= $sep.$field.\"=NULL\";\n"
        result += sp + sp + sp + "$sep = \", \";\n"
        result += sp + sp + "};\n"
    sep = "\" WHERE \""
    for field in pks:
        nice = field[1]
        getter = "getFQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        getter2 = "get" + nice[0:1].capitalize() + nice[1:] + "Name"
        if field[2] == "boolean":
            objGet = "is" + nice[0:1].capitalize() + nice[1:] + "()"
        else:
            objGet = "get" + nice[0:1].capitalize() + nice[1:] + "()"
        result += sp + sp + "$field = $this->" + getter + "();\n"
        result += sp + sp + "$field2 = $this->" + getter2 + "();\n"
        result += sp + sp + "$valueP = \":\".$field2;\n"
        result += sp + sp + "$result .= " + sep + ".$field;\n"
        result += sp + sp + "$result .= \" = \".addslashes($valueP).\"\";\n"
        sep = "\" AND \""
    result += "\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function update("
    result += "$" + objectName + ", $masked=false){\n"
    result += sp + sp + "$query = $this->buildUpdateQuery($" + objectName + ",$masked);\n\n"
    result += sp + sp + "$params = null;\n"
    result += sp + sp + "foreach($" + objectName + " as $key=>$value){\n"
    result += sp + sp + sp + "if(!is_null($value)){\n"
    result += sp + sp + sp + sp + "$params[strtoupper($key)] = $value;\n"
    result += sp + sp + sp + "}\n"
    result += sp + sp + "}\n\n"
    result += sp + sp + "$result = $this->database->query($query,$params);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors())) {\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n"
    result += sp + sp + "}\n\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    return result

#DELETE
def generateDelete(table, pks, fields):
    sp = "    "
    result = "\n" + sp + "function buildDeleteQuery($params){\n"
    result += sp + sp + "$result = \"DELETE FROM \".$this->tableName;\n\n"
    result += sp + sp + "$sep = \" WHERE \";\n"
    result += sp + sp + "foreach($params as $key=>$value) {\n"
    result += sp + sp + sp + "$result .= $sep . $key .\" = :\". $key;\n"
    result += sp + sp + sp + "$sep = \" AND \";\n"
    result += sp + sp + "}\n"
    result += "\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function delete($params){\n"
    result += sp + sp + "if(!is_array($params))\n"
    result += sp + sp + sp + "return false;\n\n"
    result += sp + sp + "$query = $this->buildDeleteQuery($params);\n\n"
    result += sp + sp + "$result = $this->database->query($query,$params);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors())) {\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n"
    result += sp + sp + "}\n\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    return result

#COUNT
def generateCount():
    sp = "    "
    result = "\n" + sp + "function buildCountQuery($criteria=null){\n"
    result += sp + sp + "$result = \"SELECT COUNT(1) FROM \".$this->tableName;\n"
    result += sp + sp + "if (!is_null($criteria)){\n"
    result += sp + sp + sp + "$result .= \" WHERE \".$criteria->toString();\n"
    result += sp + sp + "}\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function count($criteria=null){\n"
    result += sp + sp + "$query = $this->buildCountQuery($criteria);\n\n"
    result += sp + sp + "$params = null;\n"
    result += sp + sp + "if(!is_null($criteria))\n"
    result += sp + sp + sp + "$params = $criteria->getParams();\n\n"
    result += sp + sp + "$result = $this->database->single($query,$params);\n\n"
    result += sp + sp + "if(!is_null($this->database->getDbErrors())) {\n"
    result += sp + sp + sp + "return $this->database->getDbErrors();\n"
    result += sp + sp + "}\n\n"
    result += sp + sp + "return $result;\n"
    result += sp + "}\n"
    return result

#DAO HEAD
def generateDao(table, pks, fields):
    sp = "    "
    className = table[1][0:1].capitalize() + table[1][1:] + "Dao"
    result = "class " + className + " {\n\n"
    result += sp + "var $database;\n"
    result += sp + "var $tableName;\n"
    allFields = []
    allFields.extend(pks)
    allFields.extend(fields)
    for field in allFields:
        nice = field[1]
        result += sp + "var $" + nice + "Name;\n"
    result += "\n" + sp + "function " + className + "($database=null){\n"
    result += sp + sp + "$this->database = $database;\n"
    result += sp + sp + "$this->tableName = \"" + table[0] + "\";\n"
    for field in allFields:
        realn = field[0]
        nice = field[1]
        result += sp + sp + "$this->" + nice + "Name = \"" + realn + "\";\n"
    result += sp + "}\n"
    result += "\n" + sp + "function setDatabase($database){\n"
    result += sp + sp + "$this->database = $database;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function getDatabase(){\n"
    result += sp + sp + "return $this->database;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function setTableName($tableName){\n"
    result += sp + sp + "$this->tableName = $tableName;\n"
    result += sp + "}\n"
    result += "\n" + sp + "function getTableName(){\n"
    result += sp + sp + "return $this->tableName;\n"
    result += sp + "}\n"
    for field in allFields:
        nice = field[1]
        setter = "set" + nice[0:1].capitalize() + nice[1:] + "Name"
        getter = "get" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += "\n" + sp + "function " + setter + "($" + nice + "Name){\n"
        result += sp + sp + "$this->" + nice + "Name = $" + nice + "Name;\n"
        result += sp + "}\n"
        result += "\n" + sp + "function " + getter + "(){\n"
        result += sp + sp + "return $this->" + nice + "Name;\n"
        result += sp + "}\n"
    result += "\n" + sp + "function getFQFieldName($fieldName){\n"
    result += sp + sp + "$db = $this->database;\n"
    result += sp + sp + "$table = $this->tableName;\n"
    result += sp + sp + "return $db->getFQFieldName($fieldName, $table);\n"
    result += sp + "}\n"
    result += "\n" + sp + "function getQFieldName($fieldName){\n"
    result += sp + sp + "$db = $this->database;\n"
    result += sp + sp + "return $db->getQFieldName($fieldName);\n"
    result += sp + "}\n"
    for field in allFields:
        nice = field[1]
        getter = "getFQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += "\n" + sp + "function " + getter + "(){\n"
        result += sp + sp + "$db = $this->database;\n"
        result += sp + sp + "$table = $this->tableName;\n"
        result += sp + sp + "$fieldName = $this->" + nice + "Name;\n"
        result += sp + sp + "return $db->getFQFieldName($fieldName, $table);\n"
        result += sp + "}\n"
        getter = "getQ" + nice[0:1].capitalize() + nice[1:] + "Name"
        result += "\n" + sp + "function " + getter + "(){\n"
        result += sp + sp + "$db = $this->database;\n"
        result += sp + sp + "$fieldName = $this->" + nice + "Name;\n"
        result += sp + sp + "return $db->getQFieldName($fieldName);\n"
        result += sp + "}\n"
    result += generateGet(table, pks, fields)
    result += generateFind(table, pks, fields)
    result += generateInsert(table, pks, fields)
    result += generateUpdate(table, pks, fields)
    result += generateDelete(table, pks, fields)
    result += generateCount()
    #result += generateLock(table, pks, fields)
    result += "}"
    return result
