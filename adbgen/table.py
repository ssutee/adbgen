#!/usr/bin/env python

import doctest
from generator import AndroidClassGenerator
from utils import camel_variable_name

class AndroidTable(AndroidClassGenerator):
    '''
    Generate table file (XXXTable.java)
    '''
    
    def __init__(self, package, name, columns, indexes=None):
        self.package = package
        self.name = name
        self.columns = columns
        self.indexes = indexes
        self.index_create_string_vars = []
        self.index_names = []
        self.file_name = '%sTable.java' % (camel_variable_name(self.name, upper=True))
        self.string_attrs = ['name_string', 'columns_class_string', 'indexs_create_string', 
            'create_string', 'upgrade_string']
        
    def header_string(self):
        '''
        >>> table = AndroidTable('th.ac.ku.sci.cs.android.sutee.demolistview', 'dot', [])
        >>> print table.header_string()
        package th.ac.ku.sci.cs.android.sutee.demolistview;
        import android.database.sqlite.SQLiteDatabase;
        import android.provider.BaseColumns;
        <BLANKLINE>
        '''
        result = 'package ' + self.package + ';\n'
        result += 'import android.database.sqlite.SQLiteDatabase;\n'
        result += 'import android.provider.BaseColumns;\n'
        return result
        
    def class_string(self):
        '''
        >>> table = AndroidTable('th.ac.ku.sci.cs.android.sutee.demolistview', 'dot', [])
        >>> print table.class_string()
        public final class DotTable {
        %s
        }
        '''
        result  = 'public final class %sTable {\n' % (camel_variable_name(self.name, upper=True))
        result += '%s\n'
        result += '}'
        return result
        
    def name_string(self):
        '''
        >>> table = AndroidTable('th.ac.ku.sci.cs.android.sutee.demolistview', 'dot', [])
        >>> print table.name_string()
            public static final String TABLE_NAME = "dot";
        >>> table = AndroidTable('th.ac.ku.sci.cs.android.sutee.demolistview', 'dash', [])
        >>> print table.name_string()
            public static final String TABLE_NAME = "dash";
        '''
        return '    public static final String TABLE_NAME = "%s_table";' % (self.name)
        
    def columns_class_string(self):
        '''
        >>> table = AndroidTable('com.example.android', 'my_dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}])
        >>> print table.columns_class_string()
            public static class MyDotColumns implements BaseColumns {
                public static final String COORD_X = "coord_x";
                public static final String COORD_Y = "coord_y";
            }
        '''
        result = '    public static class %sColumns implements BaseColumns {\n' % (camel_variable_name(self.name, upper=True))
        for column in self.columns:
            result += '        public static final String ' + column['name'].upper() + ' = "' + column['name'] + '";\n'
        result += '    }'
        return result
        
    def upgrade_string(self):
        '''
        >>> table = AndroidTable('com.example.android', 'my_dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}])
        >>> print table.upgrade_string()
            public static void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
                db.execSQL("DROP TABLE IF EXISTS " + MyDotTable.TABLE_NAME);
                MyDotTable.onCreate(db);
            }
        >>> table = AndroidTable('com.example.android', 'my_dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}], [{'columns': ['coord_x'], 'unique': True}])
        >>> _ = table.indexs_create_string()
        >>> print table.upgrade_string()
            public static void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
                db.execSQL("DROP TABLE IF EXISTS " + MyDotTable.TABLE_NAME);
                db.execSQL("DROP INDEX IF EXISTS " + MY_DOT_COORD_X_INDEX_NAME);
                MyDotTable.onCreate(db);
            }
        '''
        result  = '    public static void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {\n'
        result += '        db.execSQL("DROP TABLE IF EXISTS " + %sTable.TABLE_NAME);\n' % (camel_variable_name(self.name, upper=True))
        for index_name in self.index_names:
            result += '        db.execSQL("DROP INDEX IF EXISTS " + %s);\n' % (index_name)        
        result += '        %sTable.onCreate(db);\n' % (camel_variable_name(self.name, upper=True))
        result += '    }'
        return result
        
    def create_string(self):
        '''
        >>> table = AndroidTable('com.example.android', 'dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}])
        >>> _ = table.indexs_create_string()
        >>> print table.create_string()
            public static void onCreate(SQLiteDatabase db) {
                StringBuilder sb = new StringBuilder();
                sb.append("CREATE TABLE " + DotTable.TABLE_NAME + " (");
                sb.append(BaseColumns._ID + " INTEGER PRIMARY KEY, ");
                sb.append(DotColumns.COORD_X + " INTEGER UNIQUE, ");
                sb.append(DotColumns.COORD_Y + " INTEGER");
                sb.append(");");
                db.execSQL(sb.toString());
            }
        >>> table = AndroidTable('com.example.android', 'dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}], [{'columns': ['coord_x'], 'unique': True}])
        >>> _ = table.indexs_create_string()
        >>> print table.create_string()
            public static void onCreate(SQLiteDatabase db) {
                StringBuilder sb = new StringBuilder();
                sb.append("CREATE TABLE " + DotTable.TABLE_NAME + " (");
                sb.append(BaseColumns._ID + " INTEGER PRIMARY KEY, ");
                sb.append(DotColumns.COORD_X + " INTEGER UNIQUE, ");
                sb.append(DotColumns.COORD_Y + " INTEGER");
                sb.append(");");
                db.execSQL(sb.toString());
                db.execSQL(INDEX_DOT_COORD_X_CREATE);
            }
        >>> table = AndroidTable('com.example.android', 'my_dot', [{'name':'coord_x','type':'integer','options':'unique'}, {'name':'coord_y','type':'integer'}], [{'columns': ['coord_x'], 'unique': True},{'columns': ['coord_x', 'coord_y'], 'unique': False}])
        >>> _ = table.indexs_create_string()
        >>> print table.create_string()
            public static void onCreate(SQLiteDatabase db) {
                StringBuilder sb = new StringBuilder();
                sb.append("CREATE TABLE " + MyDotTable.TABLE_NAME + " (");
                sb.append(BaseColumns._ID + " INTEGER PRIMARY KEY, ");
                sb.append(MyDotColumns.COORD_X + " INTEGER UNIQUE, ");
                sb.append(MyDotColumns.COORD_Y + " INTEGER");
                sb.append(");");
                db.execSQL(sb.toString());
                db.execSQL(INDEX_MY_DOT_COORD_X_CREATE);
                db.execSQL(INDEX_MY_DOT_COORD_X_COORD_Y_CREATE);
            }
        '''
        result  = '    public static void onCreate(SQLiteDatabase db) {\n'
        result += '        StringBuilder sb = new StringBuilder();\n'
        result += '        sb.append("CREATE TABLE " + %sTable.TABLE_NAME + " (");\n' % (camel_variable_name(self.name, upper=True))
        result += '        sb.append(BaseColumns._ID + " INTEGER PRIMARY KEY, ");\n'

        for index, column in enumerate(self.columns):
            tails = ''
            if 'options' in column:
                tails += ' %s' % (column['options'].upper())
            if index < len(self.columns) - 1:
                tails += ', '
            result += '        sb.append(%sColumns.%s + " %s%s");\n' % (camel_variable_name(self.name, upper=True), 
                column['name'].upper(), column['type'].upper(), tails)
        result += '        sb.append(");");\n'
        result += '        db.execSQL(sb.toString());\n'
        for index_create_string_var in self.index_create_string_vars:
            result += '        db.execSQL(%s);\n' % (index_create_string_var)
        result += '    }'
        return result

    def indexs_create_string(self):
        '''
        >>> table = AndroidTable('com.example.android', 'dot', [], [{'columns': ['coord_x'], 'unique': True}])
        >>> print table.indexs_create_string()
            private static final String DOT_COORD_X_INDEX_NAME = "dot__coord_x__idx";
            private static final String INDEX_DOT_COORD_X_CREATE = "CREATE UNIQUE INDEX "
                + DOT_COORD_X_INDEX_NAME + " ON " + DotTable.TABLE_NAME
                + " (" + DotColumns.COORD_X + ");";
        <BLANKLINE>                
        >>> table = AndroidTable('com.example.android', 'dot', [], [{'columns': ['coord_x', 'coord_y'], 'unique': False}])
        >>> print table.indexs_create_string()
            private static final String DOT_COORD_X_COORD_Y_INDEX_NAME = "dot__coord_x__coord_y__idx";
            private static final String INDEX_DOT_COORD_X_COORD_Y_CREATE = "CREATE INDEX "
                + DOT_COORD_X_COORD_Y_INDEX_NAME + " ON " + DotTable.TABLE_NAME
                + " (" + DotColumns.COORD_X + "," + DotColumns.COORD_Y + ");";
        <BLANKLINE>                
        '''
        
        def index_var_name(table_name, column_names):
            result = table_name.upper()
            for column_name in column_names:
                result += '_' + column_name.upper()
            return result + '_INDEX_NAME'
            
        def index_string_value(table_name, column_names):
            result = '"' + table_name
            for column_name in column_names:
                result += '__' + column_name            
            return result + '__idx"'
        
        def index_create_var_name(table_name, column_names):
            result = 'INDEX_' + table_name.upper()
            for column_name in column_names:
                result += '_' + column_name.upper()
            return result + '_CREATE'
            
        def index_columns_string(table_name, column_names):
            column_vars = []
            for column_name in column_names:
                column_vars.append(table_name.capitalize() + 'Columns.' + column_name.upper())
            return ' + "," + '.join(column_vars)

        if not self.indexes:
            return ''
            
        result = ''
        for index in self.indexes:
            self.index_create_string_vars.append(index_create_var_name(self.name, index['columns']))
            self.index_names.append(index_var_name(self.name, index['columns']))
            
            result += '    private static final String %s = %s;\n' % \
                (index_var_name(self.name, index['columns']), (index_string_value(self.name, index['columns'])))
            result += '    private static final String %s = "CREATE %sINDEX "\n' % \
                (index_create_var_name(self.name, index['columns']), 'UNIQUE ' if index['unique'] else '')
            result += '        + %s + " ON " + %sTable.TABLE_NAME\n' % \
                (index_var_name(self.name, index['columns']), self.name.capitalize())
            result += '        + " (" + %s + ");";\n' % (index_columns_string(self.name, index['columns']))
        return result

if __name__ == '__main__':
    doctest.testmod()    