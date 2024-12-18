// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use tauri::path::BaseDirectory;
use std::process::Command;
use tauri::Manager;

#[tauri::command]
async fn run_python(app_handle: tauri::AppHandle, invoke_message: String) -> Result<String, String> {
    let resource_dir = app_handle.path().resolve("src-python", BaseDirectory::Resource)
        .map_err(|e| e.to_string())?;
    let py_main = app_handle.path().resolve("src-python/run.py", BaseDirectory::Resource)
        .map_err(|e| e.to_string())?;
    let args: Vec<&str> = invoke_message.split(',').collect();
    match py_main.as_path().to_str() {
        Some(path) => {
            let output = Command::new("python")
                .args(std::iter::once(&path).chain(args.iter()).collect::<Vec<_>>())
                .current_dir(resource_dir.as_path().to_str().unwrap())
                .output()
                .map_err(|e| e.to_string())?;
            if output.status.success() {
                let stdout = encoding_rs::GBK.decode(&output.stdout).0.to_string();
                Ok(stdout)
            } else {
                Err(encoding_rs::GBK.decode(&output.stderr).0.to_string())
            }
        },
        None => {
            Err("Invalid path".to_string())
        },
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![run_python])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
