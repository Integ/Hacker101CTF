fn main() {
    // let codes = [53494609, 56755322, 51004373];
    for i in 0..0xFFFFFFFF {
        if check(setup(i), 53494609) {
            println!("seed:{0} --- code:{1}", i, 53494609);
        }
    }
}

fn setup(mut seed: u64) -> u64 {
	let mut state = 0;
	for _i in 0..16 {
		let cur = seed & 3;
		seed >>= 2;
		state = (state << 4) | ((state & 3) ^ cur);
		state |= cur << 2;
    }
	return state;
}

fn check(mut state: u64, code: u64) -> bool {
	for i in 0..26 {
		if (state & 1) == ((code >> (25-i)) & 1) {
            state = (state << 1) ^ (state >> 61);
            state &= 0xFFFFFFFFFFFFFFFF;
            state ^= 0xFFFFFFFFFFFFFFFF;
            for j in (0..64).step_by(4) {
                let mut cur = (state >> j) & 0xF;
                cur = (cur >> 3) | ((cur >> 2) & 2) | ((cur << 3) & 8) | ((cur << 2) & 4);
                state ^= cur << j;
            }
        } else {
            return false;
        }
    }
	return true;
}