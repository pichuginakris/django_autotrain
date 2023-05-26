console.log('fff')
document.getElementById("upload-form").addEventListener("submit", function(event) {
  let folderInput = document.getElementById("folder-input");
  let files = folderInput.files;
  for (var i = 0; i < files.length; i++) {
    let file = files[i];
    let item = document.createElement("input");
    item.type = "hidden";
    item.name = "folder_paths[]";
    item.value = file.webkitRelativePath;
    folderInput.parentNode.appendChild(item);
  }
});