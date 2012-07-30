#!/usr/bin/env python

import doctest
from generator import AndroidClassGenerator
from utils import camel_variable_name

class AndroidContentProvider(AndroidClassGenerator):
    '''
    Generate content provider file (XXXProvider.java)
    '''
    
    def __init__(self, package, prefix, tables):
        self.package = package
        self.prefix = prefix
        self.tables = tables
        self.file_name = '%sProvider.java' % (self.prefix.upper())
        self.string_attrs = ['create_string', 'get_type_string', 'insert_string', 
            'query_string', 'delete_string', 'update_string']
                
    def header_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'Test', ['user', 'group'])
        >>> print provider.header_string()
        package com.example.test;
        <BLANKLINE>
        import android.content.ContentProvider;
        import android.content.ContentResolver;
        import android.content.ContentValues;
        import android.content.UriMatcher;
        import android.database.Cursor;
        import android.database.sqlite.SQLiteDatabase;
        import android.database.sqlite.SQLiteQueryBuilder;
        import android.net.Uri;
        import android.text.TextUtils;
        import android.provider.BaseColumns;
        '''
        result  = 'package %s;\n\n' % (self.package)
        result += 'import android.content.ContentProvider;\n'
        result += 'import android.content.ContentResolver;\n'
        result += 'import android.content.ContentValues;\n'
        result += 'import android.content.UriMatcher;\n'
        result += 'import android.database.Cursor;\n'
        result += 'import android.database.sqlite.SQLiteDatabase;\n'
        result += 'import android.database.sqlite.SQLiteQueryBuilder;\n'
        result += 'import android.net.Uri;\n'
        result += 'import android.text.TextUtils;\n'
        result += 'import android.provider.BaseColumns;'
        return result
        
    def class_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'Test', ['user', 'group'])
        >>> print provider.class_string()
        public class OMUProvider extends ContentProvider {
        %s
        }
        '''
        result  = 'public class OMUProvider extends ContentProvider {\n'
        result += '%s\n'
        result += '}'
        return result
        
    def properties_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'Test', ['user', 'group'])
        >>> print provider.properties_string()
            private TestOpenHelper dbHelper;
            private SQLiteDatabase database;
            public static final String AUTHORITY = "com.example.test.contentprovider";
            private static final UriMatcher sURIMatcher = new UriMatcher(UriMatcher.NO_MATCH);
        <BLANKLINE>
            private static final int USERS = 1001;
            private static final int USER_ID = 1002;
            public static final String USER_PATH = "users";
            public static final Uri USER_CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/" + USER_PATH);
            public static final String USER_CONTENT_TYPE = ContentResolver.CURSOR_DIR_BASE_TYPE + "/users";
            public static final String USER_CONTENT_ITEM_TYPE = ContentResolver.CURSOR_ITEM_BASE_TYPE + "/user";
            static {
                sURIMatcher.addURI(AUTHORITY, USER_PATH, USERS);
                sURIMatcher.addURI(AUTHORITY, USER_PATH + "/#", USER_ID);
            }
        <BLANKLINE>
            private static final int GROUPS = 1003;
            private static final int GROUP_ID = 1004;
            public static final String GROUP_PATH = "groups";
            public static final Uri GROUP_CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/" + GROUP_PATH);
            public static final String GROUP_CONTENT_TYPE = ContentResolver.CURSOR_DIR_BASE_TYPE + "/groups";
            public static final String GROUP_CONTENT_ITEM_TYPE = ContentResolver.CURSOR_ITEM_BASE_TYPE + "/group";
            static {
                sURIMatcher.addURI(AUTHORITY, GROUP_PATH, GROUPS);
                sURIMatcher.addURI(AUTHORITY, GROUP_PATH + "/#", GROUP_ID);
            }
        <BLANKLINE>
        <BLANKLINE>
        '''
        auto_id = 1000
        result  = '    private %sOpenHelper dbHelper;\n' % (self.prefix.capitalize())
        result += '    private SQLiteDatabase database;\n'
        result += '    public static final String AUTHORITY = "%s.contentprovider";\n' % (self.package)
        result += '    private static final UriMatcher sURIMatcher = new UriMatcher(UriMatcher.NO_MATCH);\n\n'
        for table in self.tables:
            auto_id += 1
            result += '    private static final int %sS = %d;\n' % (table.upper(), auto_id)
            auto_id += 1
            result += '    private static final int %s_ID = %d;\n' % (table.upper(), auto_id)
            result += '    public static final String %s_PATH = "%ss";\n' % (table.upper(), table)
            result += '    public static final Uri %s_CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/" + %s_PATH);\n' % (table.upper(), table.upper())
            result += '    public static final String %s_CONTENT_TYPE = ContentResolver.CURSOR_DIR_BASE_TYPE + "/%ss";\n' % (table.upper(), table)
            result += '    public static final String %s_CONTENT_ITEM_TYPE = ContentResolver.CURSOR_ITEM_BASE_TYPE + "/%s";\n' % (table.upper(), table)
            result += '    static {\n'
            result += '        sURIMatcher.addURI(AUTHORITY, %s_PATH, %sS);\n' % (table.upper(), table.upper())
            result += '        sURIMatcher.addURI(AUTHORITY, %s_PATH + "/#", %s_ID);\n' % (table.upper(), table.upper())
            result += '    }\n'
            result += '\n'
        return result
    
    def create_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.create_string()
            @Override
            public boolean onCreate() {
                dbHelper = new TestOpenHelper(getContext());
                database = dbHelper.getWritableDatabase();
                return true;
            }
        '''
        result  = '    @Override\n'
        result += '    public boolean onCreate() {\n'
        result += '        dbHelper = new %sOpenHelper(getContext());\n' % (self.prefix.capitalize())
        result += '        database = dbHelper.getWritableDatabase();\n'
        result += '        return true;\n'
        result += '    }'
        return result
        
    def get_type_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.get_type_string()
            @Override
            public String getType(Uri uri) {
                int uriType = sURIMatcher.match(uri);
                switch (uriType) {
                case USERS:
                    return USER_CONTENT_TYPE;
                case USER_ID:
                    return USER_CONTENT_ITEM_TYPE;
                case GROUPS:
                    return GROUP_CONTENT_TYPE;
                case GROUP_ID:
                    return GROUP_CONTENT_ITEM_TYPE;
                }
                return null;
            }
        '''
        result  = '    @Override\n'
        result += '    public String getType(Uri uri) {\n'
        result += '        int uriType = sURIMatcher.match(uri);\n'
        result += '        switch (uriType) {\n'
        for table in self.tables:
            result += '        case %sS:\n' % (table.upper())
            result += '            return %s_CONTENT_TYPE;\n' % (table.upper())
            result += '        case %s_ID:\n' % (table.upper())
            result += '            return %s_CONTENT_ITEM_TYPE;\n' % (table.upper())            
        result += '        }\n'
        result += '        return null;\n'
        result += '    }'
        return result
        
    def insert_cases_string(self, table):
        result = '''\
        case %sS:
            id = database.insert(%sTable.TABLE_NAME, null, values);
            getContext().getContentResolver().notifyChange(uri, null);
            return Uri.parse("content://" + AUTHORITY + "/" + %s_PATH + "/" + id);\n''' % \
                (table.upper(), table.capitalize(), table.upper())
        return result    
        
    def insert_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.insert_string()
            @Override
            public Uri insert(Uri uri, ContentValues values) {
                int uriType = sURIMatcher.match(uri);
                long id = 0;
                switch (uriType) {
                case USERS:
                    id = database.insert(UserTable.TABLE_NAME, null, values);
                    getContext().getContentResolver().notifyChange(uri, null);
                    return Uri.parse("content://" + AUTHORITY + "/" + USER_PATH + "/" + id);
                case GROUPS:
                    id = database.insert(GroupTable.TABLE_NAME, null, values);
                    getContext().getContentResolver().notifyChange(uri, null);
                    return Uri.parse("content://" + AUTHORITY + "/" + GROUP_PATH + "/" + id);
                default:
                    throw new IllegalArgumentException("Unknown URI: " + uri);
                }
            }
        '''
        result = '''\
    @Override
    public Uri insert(Uri uri, ContentValues values) {
        int uriType = sURIMatcher.match(uri);
        long id = 0;
        switch (uriType) {
%s
        default:
            throw new IllegalArgumentException("Unknown URI: " + uri);
        }
    }'''
        cases = ''
        for table in self.tables:
            cases += self.insert_cases_string(table)
        return result % (cases.rstrip())
        
    def query_cases_string(self, table):
        result = '''\
        case %sS:
            queryBuilder.setTables(%sTable.TABLE_NAME);
            break;
        case %s_ID:
            queryBuilder.setTables(%sTable.TABLE_NAME);
            queryBuilder.appendWhere(BaseColumns._ID + "=" + uri.getLastPathSegment());
            break;\n''' % (table.upper(), table.capitalize(), table.upper(), table.capitalize())
        return result    
        
    def query_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.query_string()
            @Override
            public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
                int uriType = sURIMatcher.match(uri);
                SQLiteQueryBuilder queryBuilder = new SQLiteQueryBuilder();
                switch (uriType) {
                case USERS:
                    queryBuilder.setTables(UserTable.TABLE_NAME);
                    break;
                case USER_ID:
                    queryBuilder.setTables(UserTable.TABLE_NAME);
                    queryBuilder.appendWhere(BaseColumns._ID + "=" + uri.getLastPathSegment());
                    break;
                case GROUPS:
                    queryBuilder.setTables(GroupTable.TABLE_NAME);
                    break;
                case GROUP_ID:
                    queryBuilder.setTables(GroupTable.TABLE_NAME);
                    queryBuilder.appendWhere(BaseColumns._ID + "=" + uri.getLastPathSegment());
                    break;
                default:
                    throw new IllegalArgumentException("Unknown URI: " + uri);        
                }
                Cursor cursor = queryBuilder.query(database, projection, selection, selectionArgs, null, null, sortOrder);
                cursor.setNotificationUri(getContext().getContentResolver(), uri);
                return cursor;
            }
        '''
        result = '''\
    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        int uriType = sURIMatcher.match(uri);
        SQLiteQueryBuilder queryBuilder = new SQLiteQueryBuilder();
        switch (uriType) {
%s
        default:
            throw new IllegalArgumentException("Unknown URI: " + uri);        
        }
        Cursor cursor = queryBuilder.query(database, projection, selection, selectionArgs, null, null, sortOrder);
        cursor.setNotificationUri(getContext().getContentResolver(), uri);
        return cursor;
    }'''
        cases = ''
        for table in self.tables:
            cases += self.query_cases_string(table)
        return result % (cases.rstrip())
        
    def update_cases_string(self, table):
        result = '''\
        case %sS:
            rowsUpdated = database.update(%sTable.TABLE_NAME, values, selection, selectionArgs);
            break;
        case %s_ID:
            String %sId = uri.getLastPathSegment();
            if (TextUtils.isEmpty(selection)) {
                rowsUpdated = database.update(%sTable.TABLE_NAME, values, BaseColumns._ID + "=" + %sId, null);
            } else {
                rowsUpdated = database.update(%sTable.TABLE_NAME, values, BaseColumns._ID + "=" + %sId + " AND " + selection, selectionArgs);
            }
            break;\n''' % (
                table.upper(), table.capitalize(), table.upper(), camel_variable_name(table),
                table.capitalize(), camel_variable_name(table), table.capitalize(), camel_variable_name(table)
            )
        return result        
        
    def update_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.update_string()
            @Override
            public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
                int uriType = sURIMatcher.match(uri);
                int rowsUpdated = 0;
                switch (uriType) {
                case USERS:
                    rowsUpdated = database.update(UserTable.TABLE_NAME, values, selection, selectionArgs);
                    break;
                case USER_ID:
                    String userId = uri.getLastPathSegment();
                    if (TextUtils.isEmpty(selection)) {
                        rowsUpdated = database.update(UserTable.TABLE_NAME, values, BaseColumns._ID + "=" + userId, null);
                    } else {
                        rowsUpdated = database.update(UserTable.TABLE_NAME, values, BaseColumns._ID + "=" + userId + " AND " + selection, selectionArgs);
                    }
                    break;
                case GROUPS:
                    rowsUpdated = database.update(GroupTable.TABLE_NAME, values, selection, selectionArgs);
                    break;
                case GROUP_ID:
                    String groupId = uri.getLastPathSegment();
                    if (TextUtils.isEmpty(selection)) {
                        rowsUpdated = database.update(GroupTable.TABLE_NAME, values, BaseColumns._ID + "=" + groupId, null);
                    } else {
                        rowsUpdated = database.update(GroupTable.TABLE_NAME, values, BaseColumns._ID + "=" + groupId + " AND " + selection, selectionArgs);
                    }
                    break;
                default:
                    throw new IllegalArgumentException("Unknown URI: " + uri);
                }
                getContext().getContentResolver().notifyChange(uri, null);
                return rowsUpdated;
            }
        '''
        result = '''\
    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        int uriType = sURIMatcher.match(uri);
        int rowsUpdated = 0;
        switch (uriType) {
%s
        default:
            throw new IllegalArgumentException("Unknown URI: " + uri);
        }
        getContext().getContentResolver().notifyChange(uri, null);
        return rowsUpdated;
    }'''
        cases = ''
        for table in self.tables:
            cases += self.update_cases_string(table)
        return result % (cases.rstrip())

    def delete_cases_string(self, table):
        result = '''\
        case %sS:
            rowsDeleted = database.delete(%sTable.TABLE_NAME, selection, selectionArgs);
            break;
        case %s_ID:
            String %sId = uri.getLastPathSegment();
            if (TextUtils.isEmpty(selection)) {
                rowsDeleted = database.delete(%sTable.TABLE_NAME, BaseColumns._ID + "=" + %sId, null);
            } else {
                rowsDeleted = database.delete(%sTable.TABLE_NAME, BaseColumns._ID + "=" + %sId + " AND " + selection, selectionArgs);
            }
            break;\n''' % (
                table.upper(), table.capitalize(), table.upper(), camel_variable_name(table),
                table.capitalize(), camel_variable_name(table), table.capitalize(), camel_variable_name(table)
            )
        return result
        
    def delete_string(self):
        '''
        >>> provider = AndroidContentProvider('com.example.test', 'test', ['user', 'group'])
        >>> print provider.delete_string() 
            @Override
            public int delete(Uri uri, String selection, String[] selectionArgs) {
                int uriType = sURIMatcher.match(uri);
                int rowsDeleted = 0;
                switch (uriType) {
                case USERS:
                    rowsDeleted = database.delete(UserTable.TABLE_NAME, selection, selectionArgs);
                    break;
                case USER_ID:
                    String userId = uri.getLastPathSegment();
                    if (TextUtils.isEmpty(selection)) {
                        rowsDeleted = database.delete(UserTable.TABLE_NAME, BaseColumns._ID + "=" + userId, null);
                    } else {
                        rowsDeleted = database.delete(UserTable.TABLE_NAME, BaseColumns._ID + "=" + userId + " AND " + selection, selectionArgs);
                    }
                    break;
                case GROUPS:
                    rowsDeleted = database.delete(GroupTable.TABLE_NAME, selection, selectionArgs);
                    break;
                case GROUP_ID:
                    String groupId = uri.getLastPathSegment();
                    if (TextUtils.isEmpty(selection)) {
                        rowsDeleted = database.delete(GroupTable.TABLE_NAME, BaseColumns._ID + "=" + groupId, null);
                    } else {
                        rowsDeleted = database.delete(GroupTable.TABLE_NAME, BaseColumns._ID + "=" + groupId + " AND " + selection, selectionArgs);
                    }
                    break;
                default:
                    throw new IllegalArgumentException("Unknown URI: " + uri);      
                }
                getContext().getContentResolver().notifyChange(uri, null);
                return rowsDeleted;
            }
        '''
        result = '''\
    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        int uriType = sURIMatcher.match(uri);
        int rowsDeleted = 0;
        switch (uriType) {
%s
        default:
            throw new IllegalArgumentException("Unknown URI: " + uri);      
        }
        getContext().getContentResolver().notifyChange(uri, null);
        return rowsDeleted;
    }'''
        cases = ''
        for table in self.tables:
            cases += self.delete_cases_string(table)
        return result % (cases.rstrip())

if __name__ == '__main__':
    doctest.testmod()
    