use rand::rngs::OsRng;
use pqc_kyber::*;
use std::ptr;

#[no_mangle]
pub extern "C" fn encapsulate_key(
    public_key_ptr: *const u8,   // Input: Pointer to client's public key
    ciphertext_ptr: *mut u8,     // Output: Pointer to buffer for ciphertext
    shared_secret_ptr: *mut u8,  // Output: Pointer to buffer for shared secret
) -> i32 {
    // Safety checks for pointers
    if public_key_ptr.is_null() || ciphertext_ptr.is_null() || shared_secret_ptr.is_null() {
        return -1; // Error: Null pointer
    }

    let mut rng = OsRng;

    unsafe {
        // Reconstruct the public key slice from the pointer
        let public_key = std::slice::from_raw_parts(public_key_ptr, KYBER_PUBLICKEYBYTES);
        
        // Prepare buffers for ciphertext and shared secret
        let mut ciphertext = [0u8; KYBER_CIPHERTEXTBYTES];
        let mut shared_secret = [0u8; 32];

        // Call the encapsulate function
        match encapsulate(public_key, &mut rng) {
            Ok((ct, ss)) => {
                // Copy the ciphertext and shared secret to the provided buffers
                ciphertext.copy_from_slice(&ct);
                shared_secret.copy_from_slice(&ss);

                ptr::copy_nonoverlapping(ciphertext.as_ptr(), ciphertext_ptr, KYBER_CIPHERTEXTBYTES);
                ptr::copy_nonoverlapping(shared_secret.as_ptr(), shared_secret_ptr, 32);

                0 // Success
            },
            Err(_) => -2, // Error: Encapsulation failed
        }
    }
}

