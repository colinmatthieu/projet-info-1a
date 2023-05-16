#![allow(non_snake_case)]

use std::path::PathBuf;

use notify::{Watcher, RecursiveMode, watcher, DebouncedEvent};
use std::sync::mpsc::channel;
use std::time::Duration;
use std::thread;

#[tokio::main]
async fn main() 
{
    let mut dataPath = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    dataPath.push("../TestData");
    println!("Data path: {}", dataPath.display());
    
    /////////////FILE WATCHER///////////////////////////
    let (sender, receiver) = channel();
    // Create a watcher object, delivering debounced events. The notification back-end is selected based on the platform.
    let mut watcher = watcher(sender, Duration::from_secs(3)).unwrap();
    // Add a path to be watched. All files and directories at that path and below will be monitored for changes.
    watcher.watch(dataPath, RecursiveMode::Recursive).unwrap();

    loop {
        match receiver.recv() {
           Ok(event) => {
            println!("modif: {:?}", event);
            if let DebouncedEvent::Write(p) = event{
                println!("Modified file{:?}",p);
                thread::spawn(|| {process(p);});
            }
            
           },
           Err(e) => println!("watch error: {:?}", e),
        }
    }
}

use error_chain::error_chain;
//use serde::Deserialize;
use serde_json::json;
use std::env;
use reqwest::blocking::Client;
use std::fs;

error_chain! {
    foreign_links {
        EnvVar(env::VarError);
        HttpRequest(reqwest::Error);
    }
}
use std::fs::metadata;
fn process(filePath:PathBuf)->Result<()>{
    let md = metadata(&filePath).unwrap();
    if md.is_dir() {
        println!("Ignoring directory: {:?}", filePath);
        return Ok(())
    }
    let contents = fs::read_to_string(&filePath)
        .expect("Should have been able to read the file");
        
    let data = json!({
        "fridgeName": "arthurooo",
        "path": filePath.into_os_string().into_string(),
        "contents": contents,
        "files": {
             "file1": {
             "content": r#"trucs"#
            }
        }});

    let request_url = "http://localhost:5000/sendData";
    println!("about to send server data");
    let _response = Client::new()
        .post(request_url)
        //.basic_auth(gh_user.clone(), Some(gh_pass.clone())) //todo: handle auth
        .json(&data)
        .send();//.await?;
    println!("sent !!");

    //let result = response.json().await?;
    
    Ok(())
}