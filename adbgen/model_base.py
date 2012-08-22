#!/usr/bin/env python

import doctest
from generator import AndroidClassGenerator
from utils import camel_variable_name

class AndroidModelBase(AndroidClassGenerator):
    '''
    Generate model base file ([TableName].java)
    '''
    
    def __init__(self, package, table, columns):
        self.package = package
        self.table = table
        self.columns = columns
        self.file_name = '%s.java' % (camel_variable_name(self.table, upper=True))
        self.string_attrs = ['properties_string','constructor_string','get_id_string',
            'from_cursor_string','to_content_values_string', 'new_instance_from_cursor_string']
        
    def header_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'Album', [])
        >>> print model_base.header_string()
        package com.touchsi.android.opd.model;
        import android.provider.BaseColumns;
        import android.content.ContentValues;
        import android.content.Context;
        import android.database.Cursor;
        '''
        result = '''\
package %s;
import android.provider.BaseColumns;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;''' % (self.package)
        return result

    def class_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'Album', [{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.class_string()
        public class Album extends ModelBase {
        %s
        }
        '''
        result  = 'public class %s extends ModelBase {\n' % (camel_variable_name(self.table, upper=True))
        result += '%s\n'
        result += '}'
        return result

    def properties_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'Album', [{"name": "done","type": "boolean"},{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.properties_string()
            private Context context;
            private int id;
            private boolean done;
            private String name;
            private Date addedAt;
            private Date updatedAt;
        <BLANKLINE>
        '''
        import re
        result  = '    private Context context;\n'
        result += '    private int id;\n'
        for column in self.columns:
            var_type = 'Object'
            if re.match(r'varchar.*',column['type']) or column['type'] == 'text':
                var_type = 'String'
            elif column['type'] == 'integer':
                var_type = 'int'
            elif column['type'] == 'timestamp':
                var_type = 'Date'
            elif column['type'] == 'float':
                var_type = 'float'
            elif column['type'] == 'boolean':
                var_type = 'boolean'
                
            result += '    private %s %s;\n' % (var_type, camel_variable_name(column['name']))
        return result
        
    def constructor_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'Album', [{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.constructor_string()
            public Album() {
                super();
            }
        '''
        return '''\
    public %s() {
        super();
    }''' % (camel_variable_name(self.table, upper=True))
    
    def get_id_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'Album', [{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.get_id_string()        
            @Override
            public int getId() {
                return id;
            }
        '''
        return '''\
    @Override
    public int getId() {
        return id;
    }'''
    
    def new_instance_from_cursor_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'my_book', [{"name": "done","type": "boolean"},{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.new_instance_from_cursor_string()
            public static MyBook newInstance(Cursor cursor, Context context) {
                MyBook myBook = new MyBook();
                myBook.fromCursor(cursor, context);
                return myBook;
            }
        '''
        result  = '    public static %s newInstance(Cursor cursor, Context context) {\n' % (camel_variable_name(self.table, upper=True))
        result += '        %s %s = new %s();\n' % (camel_variable_name(self.table, upper=True), camel_variable_name(self.table, upper=False), camel_variable_name(self.table, upper=True))
        result += '        %s.fromCursor(cursor, context);\n' % (camel_variable_name(self.table, upper=False))
        result += '        return %s;\n' % (camel_variable_name(self.table, upper=False))
        result += '    }'
        return result
    
    def from_cursor_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'my_book', [{"name": "done","type": "boolean"},{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.from_cursor_string()
            @Override
            public void fromCursor(Cursor cursor, Context context) {
                this.id = cursor.getInt(cursor.getColumnIndex(BaseColumns._ID));
                this.done = cursor.getInt(cursor.getColumnIndex(MyBookTable.MyBookColumns.DONE)) == 1;
                this.name = cursor.getString(cursor.getColumnIndex(MyBookTable.MyBookColumns.NAME));
                this.addedAt = new Date(cursor.getLong(cursor.getColumnIndex(MyBookTable.MyBookColumns.ADDED_AT)));
                this.updatedAt = new Date(cursor.getLong(cursor.getColumnIndex(MyBookTable.MyBookColumns.UPDATED_AT)));
                this.context = context;
            }
        '''
        import re
        result  = '    @Override\n'
        result += '    public void fromCursor(Cursor cursor, Context context) {\n'
        result += '        this.id = cursor.getInt(cursor.getColumnIndex(BaseColumns._ID));\n'
        for column in self.columns:
            result += '        this.%s = ' % (camel_variable_name(column['name']))
            column_index = 'cursor.getColumnIndex(%sTable.%sColumns.%s)' % (camel_variable_name(self.table, upper=True), camel_variable_name(self.table, upper=True), column['name'].upper())
            if re.match(r'varchar.*',column['type']) or column['type'] == 'text':
                result += 'cursor.getString(%s);\n' % (column_index)
            elif column['type'] == 'integer':
                result += 'cursor.getInt(%s);\n' % (column_index)
            elif column['type'] == 'timestamp':
                result += 'new Date(cursor.getLong(%s));\n' % (column_index)
            elif column['type'] == 'float':
                result += 'cursor.getFloat(%s);\n' % (column_index)
            elif column['type'] == 'boolean':
                result += 'cursor.getInt(%s) == 1;\n' % (column_index)
        result += '        this.context = context;\n'
        result += '    }'
        return result
        
    def to_content_values_string(self):
        '''
        >>> model_base = AndroidModelBase('com.touchsi.android.opd.model', 'my_book', [{"name": "done","type": "boolean"},{"name": "name","type": "varchar(100)","options": "unique"},{"name": "added_at","type": "timestamp","options": "default current_timestamp"},{"name": "updated_at","type": "timestamp","options": "default current_timestamp"}])
        >>> print model_base.to_content_values_string()
            @Override
            public ContentValues toContentValues() {
                ContentValues values = new ContentValues();
                values.put(MyBookTable.MyBookColumns.DONE, this.done);
                values.put(MyBookTable.MyBookColumns.NAME, this.name);
                values.put(MyBookTable.MyBookColumns.ADDED_AT, this.addedAt.getTime());
                values.put(MyBookTable.MyBookColumns.UPDATED_AT, this.updatedAt.getTime());
            	return values;
            }
        '''
        result  = '    @Override\n'
        result += '    public ContentValues toContentValues() {\n'
        result += '        ContentValues values = new ContentValues();\n'
        for column in self.columns:
            if column['type'] == 'timestamp':
                result += '        values.put(%sTable.%sColumns.%s, this.%s.getTime());\n' % (camel_variable_name(self.table, upper=True), camel_variable_name(self.table, upper=True), column['name'].upper(), camel_variable_name(column['name']))
            else:
                result += '        values.put(%sTable.%sColumns.%s, this.%s);\n' % (camel_variable_name(self.table, upper=True), camel_variable_name(self.table, upper=True), column['name'].upper(), camel_variable_name(column['name']))
        result += '        return values;\n'
        result += '    }'
        return result

if __name__ == '__main__':
    doctest.testmod()