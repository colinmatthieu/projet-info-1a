#![allow(non_snake_case)]

use std::path::PathBuf;

use notify::{Watcher, RecursiveMode, watcher};
use std::sync::mpsc::channel;
use std::time::Duration;

#[tokio::main]
async fn main() 
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
           Ok(event) => {
            println!("modif: {:?}", event);
            process().await;
           },
           Err(e) => println!("watch error: {:?}", e),
        }
    }
}

use error_chain::error_chain;
use serde::Deserialize;
use serde_json::json;
use std::env;
use reqwest::Client;

error_chain! {
    foreign_links {
        EnvVar(env::VarError);
        HttpRequest(reqwest::Error);
    }
}

//#[derive(Deserialize, Debug)]
struct Gist {
    id: String,
    html_url: String,
}

async fn process()->Result<()>{
    let gist_body = json!({
        "nm": "arthurooo",
        "description": "on va mettre nos data ici je pense",
        "public": true,
        "files": {
             "main.rs": {
             "content": r#"fn main() { println!("hello world!");}"#
            }
        }});

    let request_url = "http://localhost:5000/sendData";
    println!("about to send server data");
    let response = Client::new()
        .post(request_url)
        //.basic_auth(gh_user.clone(), Some(gh_pass.clone()))
        .json(&gist_body)
        .send().await?;
    println!("sent !!");

    //let gist: Gist = response.json().await?;
    //println!("Created {:?}", gist);
    
    Ok(())
}