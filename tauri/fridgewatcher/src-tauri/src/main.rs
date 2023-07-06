use tauri::{SystemTray, SystemTrayMenu, SystemTrayEvent};
use tauri::Manager;

use std::path::PathBuf;
use notify::{Watcher, RecursiveMode, watcher, DebouncedEvent};
use std::sync::mpsc::channel;
use std::time::Duration;
use std::thread;

#[allow(non_snake_case)]
// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#[cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tokio::main]
async fn start_logger() 
{
    println!("In logger");
    let mut dataPath = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    dataPath.push("..");
    dataPath.push("..");
    dataPath.push("..");
    dataPath.push("TestData");
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

#[tauri::command]
fn start_tauri_logger() {
    println!("In tauri logger");
    start_logger();
}

fn main() {
  let tray_menu = SystemTrayMenu::new(); // insert the menu items here
  tauri::Builder::default()
    .system_tray(SystemTray::new().with_menu(tray_menu))
    .on_system_tray_event(|app, event| match event {
      SystemTrayEvent::LeftClick {
        position: _,
        size: _,
        ..
      } => {
        println!("system tray received a left click");
      }
      SystemTrayEvent::RightClick {
        position: _,
        size: _,
        ..
      } => {
        println!("system tray received a right click");
      }
      SystemTrayEvent::DoubleClick {
        position: _,
        size: _,
        ..
      } => {
        println!("system tray received a double click");
      }
      SystemTrayEvent::MenuItemClick { id, .. } => {
        match id.as_str() {
          "quit" => {
            std::process::exit(0);
          }
          "hide" => {
            let window = app.get_window("main").unwrap();
            window.hide().unwrap();
          }
          _ => {}
        }
      }
      _ => {}
    })
    .invoke_handler(tauri::generate_handler![greet, start_tauri_logger])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}