// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use pyo3::prelude::*;
use pyo3::types::IntoPyDict;
use pyo3::ffi::c_str;
    
#[tauri::command]
fn greet() -> String {
    let res: Result<String, PyErr> = Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let version: String = sys.getattr("version")?.extract()?;

        let locals = [("os", py.import("os")?)].into_py_dict(py)?;
        let code = c_str!("os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'");
        let user: String = py.eval(code, None, Some(&locals))?.extract()?;

        Ok(format!("Hello {}, I'm Python {}", user, version))
    });
    match res {
        Ok(s) => s,
        Err(e) => format!("Python error: {}", e),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
