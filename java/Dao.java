package com.touchsi.android.opd.model;

import java.util.ArrayList;
import java.util.List;

import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

public class Dao<T extends ModelBase> {

	private Context mContext;
	private Uri mContentUri;
	private Class<T> mClazz;
	private String mSelection;
	private String mSortOrder;

	public Dao(Class<T> clazz, Context context, Uri contentUri,
			String selection, String sortOrder) {
		mContext = context;
		mContentUri = contentUri;
		mClazz = clazz;
		mSelection = selection;
		mSortOrder = sortOrder;
	}

	public Dao(Class<T> clazz, Context context, Uri contentUri, String selection) {
		this(clazz, context, contentUri, selection, null);
	}

	public Dao(Class<T> clazz, Context context, Uri contentUri) {
		this(clazz, context, contentUri, null);
	}

	public T getById(int id) {
		String selection = mSelection == null ? "_id = " + id : "_id = " + id
				+ " AND " + mSelection;

		Cursor cursor = mContext.getContentResolver().query(mContentUri, null,
				selection, null, mSortOrder);

		if (cursor.getCount() == 0) {
			cursor.close();
			return null;
		}

		cursor.moveToFirst();
		T object = null;
		try {
			object = mClazz.newInstance();
			object.fromCursor(cursor, mContext);
		} catch (InstantiationException e) {
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			e.printStackTrace();
		}

		cursor.close();
		return object;
	}

	public T get(int position) {
		Cursor cursor = mContext.getContentResolver().query(mContentUri, null,
				mSelection, null, mSortOrder);
		cursor.moveToPosition(position);
		try {
			T object = mClazz.newInstance();
			object.fromCursor(cursor, mContext);
			cursor.close();
			return object;
		} catch (IllegalAccessException e) {
			e.printStackTrace();
		} catch (InstantiationException e) {
			e.printStackTrace();
		}
		cursor.close();
		return null;
	}

	public List<T> get(String selection, String[] seletecionArgs) {
		ArrayList<T> results = new ArrayList<T>();
		String mergedSelection = null;
		if (selection != null && mSelection == null) {
			mergedSelection = selection;
		} else if (selection == null && mSelection != null) {
			mergedSelection = mSelection;
		} else if (selection != null && mSelection != null) {
			mergedSelection = mSelection + " AND " + selection;
		}
		Cursor cursor = mContext.getContentResolver().query(mContentUri, null,
				mergedSelection, seletecionArgs, mSortOrder);
		cursor.moveToFirst();
		while (!cursor.isAfterLast()) {
			try {
				T object = mClazz.newInstance();
				object.fromCursor(cursor, mContext);
				results.add(object);
				cursor.moveToNext();
			} catch (IllegalAccessException e) {
				e.printStackTrace();
			} catch (InstantiationException e) {
				e.printStackTrace();
			}
		}
		cursor.close();
		return results;
	}

	public int size() {
		Cursor cursor = mContext.getContentResolver().query(mContentUri, null,
				mSelection, null, null);
		int size = cursor.getCount();
		cursor.close();
		return size;
	}

	public Uri insert(T object) {
		return mContext.getContentResolver().insert(mContentUri,
				object.toContentValues());
	}

	public int update(T object) {
		return mContext.getContentResolver().update(
				Uri.withAppendedPath(mContentUri,
						String.valueOf(object.getId())),
				object.toContentValues(), null, null);
	}

	public int delete(T object) {
		return mContext.getContentResolver().delete(
				Uri.withAppendedPath(mContentUri,
						String.valueOf(object.getId())), null, null);
	}

	public void destroy() {
		mContext.getContentResolver().delete(mContentUri, null, null);
	}
}
