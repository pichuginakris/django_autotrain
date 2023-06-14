document.getElementById("upload-form").addEventListener("submit", function(event) {
    let flagDepth = "False"; // флаг, который определяет, есть ли в папке еще хотя бы одна вложенная папка
    let folderInput = document.getElementById("folder-input");
    let files = folderInput.files;
    for (var i = 0; i < files.length; i++) {
        let file = files[i];
        let item = document.createElement("input");
        item.type = "hidden";
        item.name = "folder_paths[]";
        item.value = file.webkitRelativePath;
        let folderDepth = item.value.split("/").length - 1;
        console.log(item.value);
        console.log(folderDepth);
        if (folderDepth > 1) {
              flagDepth = "True";
      }

    folderInput.parentNode.appendChild(item);
    }
    if (flagDepth === "False") {
        // Вывод текста ошибки в upload-form
          let errorText = document.getElementById("launch-files-text");
          errorText.textContent = "Ошибка: вложенность папки меньше одной.";
          errorText.style.color = "red";
          item.value ='fafsafas';
          folderInput.parentNode.appendChild(errorText);
          event.preventDefault(); // Отмена отправки запроса POST
          return;
     }
});
