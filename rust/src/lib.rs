use std::{mem, thread};
use std::os::raw::{c_char, c_void};
use std::ops::Deref;
use std::ptr;

type Callback = extern fn(*mut c_void, SizedString);

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

struct Sendable(*mut c_void);

unsafe impl Send for Sendable {}

impl Deref for Sendable {
    type Target = *mut c_void;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[no_mangle]
pub unsafe extern "C" fn process(
    bytes: *mut u8, len: usize, cb: Callback, h: *mut c_void)
{
    // copy the bytes because we need ownership over them
    let mut copied_bytes = Vec::with_capacity(len);
    copied_bytes.set_len(len);
    ptr::copy(bytes, copied_bytes.as_mut_ptr(), len);

    // create owned string so we can pass it between threads
    let s = String::from_utf8(copied_bytes).unwrap();

    // make handle `Send`able too
    let s_h = Sendable(h);

    thread::spawn(move || {
        let ss = SizedString::from(s);
        cb(*s_h, ss);
    });
}
