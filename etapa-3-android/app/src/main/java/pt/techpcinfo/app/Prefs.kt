package pt.techpcinfo.app

import android.content.Context

object Prefs {
    private const val NAME = "techpcinfo"
    private const val KEY_URL = "server_url"
    const val DEFAULT_URL = "http://10.0.2.2:8080"

    fun getServerUrl(ctx: Context): String {
        val p = ctx.getSharedPreferences(NAME, Context.MODE_PRIVATE)
        return p.getString(KEY_URL, DEFAULT_URL)?.trim()?.trimEnd('/') ?: DEFAULT_URL
    }

    fun setServerUrl(ctx: Context, url: String) {
        ctx.getSharedPreferences(NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_URL, url.trim().trimEnd('/'))
            .apply()
    }
}
