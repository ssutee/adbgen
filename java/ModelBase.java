package com.touchsi.android.opd.model;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;

abstract public class ModelBase {

	public ModelBase() {
		super();
	}
	
	abstract public void fromCursor(Cursor cursor, Context context);
	abstract public int getId();
	abstract public ContentValues toContentValues();

}