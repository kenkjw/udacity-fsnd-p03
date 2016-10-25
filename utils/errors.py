"""
Utility methods for converting an error message short string to a 
short code for sending through a query string and then converting
the short code back into a long error message string.

get(SHORT_STRING) -> error_code
get(error_code) -> Long error string.

"""
_error_codes = dict()
_error_strings = dict()

def get(key):
    try:
        int(key)
        return _error_strings.get(key,_error_strings["00"])
    except ValueError:
        return _error_codes.get(key,"00")
    

def get_str(key):
    return _error_strings.get(_error_codes.get(key))

def set(key,code,string):
    _error_codes[key] = code;
    _error_strings[code] = string


set("POST_NOT_FOUND","01","Unable to find post.")
set("POST_INCOMPLETE_FORM","02","You must fill out the form")
set("POST_NO_PERMISSION_EDIT","03",
    "You do not have the permission to edit this post.")
set("POST_NO_PERMISSION_DELETE","04",
    "You do not have the permission to delete this post.")
set("POST_LIKE_OWN","05","You cannot like your own post.")

set("COMMENT_NOT_FOUND","10","Unable to find comment.")
set("COMMENT_NO_PERMISSION_DELETE","11",
    "You do not have the permission to delete this comment.")
set("COMMENT_NO_PERMISSION_DELETE","12",
    "You do not have the permission to edit this comment.")

set("USER_NOT_FOUND","20","Unable to find user.")

set("UNKNOWN_ERROR","00","There was an unknown error in your request.")