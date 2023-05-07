#![allow(non_snake_case)]

use std::path::PathBuf;

use notify::{Watcher, RecursiveMode, watcher};
use std::sync::mpsc::channel;
use std::time::Duration;

fn main() 
{
    let mut dataPath = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    dataPath.push("../TestData");
    println!("Data path: {}", dataPath.display());
    
    /////////////FILE WATCHER///////////////////////////
    let (sender, receiver) = channel();

    // Create a watcher object, delivering debounced events.
    // The notification back-end is selected based on the platform.
    let mut watcher = watcher(sender, Duration::from_secs(10)).unwrap();

    // Add a path to be watched. All files and directories at that path and
    // below will be monitored for changes.
    watcher.watch(dataPath, RecursiveMode::Recursive).unwrap();

    loop {
        match receiver.recv() {
           Ok(event) => println!("modif: {:?}", event),
           Err(e) => println!("watch error: {:?}", e),
        }
    }
}
