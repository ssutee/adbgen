#!/usr/bin/env python

import doctest
from generator import AndroidClassGenerator
from utils import camel_variable_name

class AndroidOpenHelper(AndroidClassGenerator):
    '''
    Generate open helper file (XXXOpenHelper.java)
    '''
    
    def __init__(self, package, prefix, db_name, tables):
        self.package = package
        self.prefix = prefix
        self.tables = tables
        self.db_name = db_name
        self.file_name = '%sOpenHelper.java' % (camel_variable_name(self.prefix, upper=True))
        self.string_attrs = ['properties_string', 'constructor_string', 'create_string', 'upgrade_string']
                        
    def header_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'Test', 'test.db', ['user','group'])
        >>> print helper.header_string()
        package com.example.dot;
        <BLANKLINE>
        import android.content.Context;
        import android.database.sqlite.SQLiteDatabase;
        import android.database.sqlite.SQLiteOpenHelper;
        '''
        result  = 'package %s;\n\n' % (self.package)
        result += 'import android.content.Context;\n'
        result += 'import android.database.sqlite.SQLiteDatabase;\n'
        result += 'import android.database.sqlite.SQLiteOpenHelper;'
        return result
    
    def class_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'Test', 'test.db', ['user','group'])
        >>> print helper.class_string()
        public class TestOpenHelper extends SQLiteOpenHelper {
        %s
        }
        '''
        result  = 'public class %sOpenHelper extends SQLiteOpenHelper {\n' % (camel_variable_name(self.prefix, upper=True))
        result += '%s\n'
        result += '}'
        return result
        
    def properties_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'test', 'test.db', ['user','group'])
        >>> print helper.properties_string()        
            private static final String DATABASE_NAME = "test.db";
            private static final int DATABASE_VERSION = 1;
        '''
        result  = '    private static final String DATABASE_NAME = "%s";\n' % (self.db_name)
        result += '    private static final int DATABASE_VERSION = 1;'
        return result
        
    def constructor_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'test', 'test.db', ['user','group'])
        >>> print helper.constructor_string()
            public TestOpenHelper(Context context) {
                super(context, DATABASE_NAME, null, DATABASE_VERSION);
            }
        '''
        result  = '    public %sOpenHelper(Context context) {\n' % (camel_variable_name(self.prefix, upper=True))
        result += '        super(context, DATABASE_NAME, null, DATABASE_VERSION);\n'
        result += '    }'
        return result
        
    def create_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'test', 'test.db', ['user','group'])
        >>> print helper.create_string()
            @Override
            public void onCreate(SQLiteDatabase db) {
                UserTable.onCreate(db);
                GroupTable.onCreate(db);
            }
        '''
        result  = '    @Override\n'
        result += '    public void onCreate(SQLiteDatabase db) {\n'
        for table in self.tables:
            result += '        %sTable.onCreate(db);\n' % (camel_variable_name(table, upper=True))
        result += '    }'
        return result

    def upgrade_string(self):
        '''
        >>> helper = AndroidOpenHelper('com.example.dot', 'test', 'test.db', ['user','group'])
        >>> print helper.upgrade_string()
            @Override
            public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
                UserTable.onUpgrade(db, oldVersion, newVersion);
                GroupTable.onUpgrade(db, oldVersion, newVersion);
            }
        '''
        result  = '    @Override\n'
        result += '    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {\n'
        for table in self.tables:
            result += '        %sTable.onUpgrade(db, oldVersion, newVersion);\n' % (camel_variable_name(table, upper=True))        
        result += '    }'
        return result
                
if __name__ == '__main__':
    doctest.testmod()
    