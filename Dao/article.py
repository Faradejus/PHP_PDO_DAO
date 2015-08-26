#!/usr/bin/env python
# -*- coding: utf-8 -*-
import phpDaoGenerator


table = ("article", "article")
pks = []
pks.append(("aid", "id", "numeric"))
fields = []
fields.append(("subcatid", "subcategoryId", "numeric"))
fields.append(("title", "title", "string"))
fields.append(("content", "content", "text"))
fields.append(("small_image", "smallImage", "text"))
fields.append(("small_image_type", "smallImageType", "string"))
fields.append(("middle_image", "middleImage", "text"))
fields.append(("middle_image_type", "middleImageType", "string"))

fields.append(("created_uid", "createdUserId", "numeric"))

fields.append(("created_date", "createdDate", "string"))
fields.append(("updated_date", "updatedDate", "string"))
fields.append(("first_page_date", "firstPageDate", "string"))

fields.append(("active", "active", "boolean"))
fields.append(("sort", "sort", "numeric"))

if __name__ == '__main__':
    f = open(table[1] + "Dao.class.php", "w")
    f.write("<?php\n\n")
    f.write(phpDaoGenerator.generateBean(table, pks, fields))
    f.write("\n")
    f.write(phpDaoGenerator.generateDao(table, pks, fields))
    f.write("\n\n?>")

