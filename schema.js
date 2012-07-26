{
    "package": "com.touchsi.android.opd.model",
    "prefix": "OMU",
    "database": "omu.db",
    "tables": ["album", "content"],
    "album": {
        "columns": [
        {
            "name": "name",
            "type": "varchar(100)",
            "options": "unique"
        },
        {
            "name": "added_at",
            "type": "timestamp",
            "options": "default current_timestamp"
        },
        {
            "name": "updated_at",
            "type": "timestamp",
            "options": "default current_timestamp"
        }
        ],
        "indexes": [
        {
            "columns": ["name"],
            "unique": true
        }
        ]
    },
    "content": {
        "columns": [
        {
            "name": "album_id",
            "type": "integer"
        },
        {
            "name": "type",
            "type": "integer"
        },
        {
            "name": "uri",
            "type": "varchar(100)"
        },
        {
            "name": "description",
            "type": "varchar(1024)"
        },
        {
            "name": "added_at",
            "type": "timestamp",
            "options": "default current_timestamp"
        },
        {
            "name": "updated_at",
            "type": "timestamp",
            "options": "default current_timestamp"
        }
        ],
        "indexes": [
        {
            "columns": ["album_id"],
            "unique": false
        },
        {
            "columns": ["album_id", "type"],
            "unique": false
        }
        ]
    }
}