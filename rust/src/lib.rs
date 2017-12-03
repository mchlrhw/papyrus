use std::mem;
use std::os::raw::c_char;

#[repr(C)]
pub struct SizedString {
    pub data: *mut c_char,
    pub len: usize,
}

impl From<String> for SizedString {
    fn from(mut s: String) -> Self {
        s.shrink_to_fit();
        let rv = Self {
            data: s.as_ptr() as *mut c_char,
            len: s.len(),
        };
        mem::forget(s);
        rv
    }
}

#[no_mangle]
pub unsafe extern "C" fn process(bytes: *const c_char, len: usize) -> SizedString {
    let s = String::from_raw_parts(bytes as *mut _, len, len);
    SizedString::from(s)
}
