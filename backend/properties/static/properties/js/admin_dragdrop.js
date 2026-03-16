(function() {
  'use strict';

  function initPropertyImageDropzone() {
    var inlineGroup = document.querySelector('#propertyimage_set-group') ||
                      document.querySelector('#propertyimage-group') ||
                      document.querySelector('#images-group');
    if (!inlineGroup) {
      var groups = document.querySelectorAll('.js-inline-admin-formset');
      for (var g = 0; g < groups.length; g++) {
        var inputs = groups[g].querySelectorAll('input[type="file"][name*="image"]');
        if (inputs.length) {
          inlineGroup = groups[g];
          break;
        }
      }
    }
    if (!inlineGroup) return;

    var wrapper = inlineGroup.querySelector('.wrapper');
    if (!wrapper) return;

    var fileInputs = inlineGroup.querySelectorAll('input[type="file"][name*="image"]');
    if (!fileInputs.length) return;

    var addLink = inlineGroup.querySelector('.add-row a.addlink, tr.add-row a.addlink');
    if (!addLink) return;

    var dropzone = document.createElement('div');
    dropzone.className = 'property-image-dropzone';
    dropzone.setAttribute('role', 'button');
    dropzone.setAttribute('tabindex', '0');
    dropzone.innerHTML = '<div class="dropzone-icon">📷</div><p>Drop images here or click to browse</p>';
    wrapper.parentNode.insertBefore(dropzone, wrapper);

    function getEmptyFileInputs() {
      var inputs = inlineGroup.querySelectorAll('input[type="file"][name*="image"]');
      var empty = [];
      for (var i = 0; i < inputs.length; i++) {
        if (!inputs[i].value && !inputs[i].files.length) {
          empty.push(inputs[i]);
        }
      }
      return empty;
    }

    function assignFileToInput(input, file) {
      try {
        var dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
      } catch (e) {
        return false;
      }
    }

    function handleFiles(files) {
      var validFiles = [];
      for (var i = 0; i < files.length; i++) {
        var f = files[i];
        if (f.type.indexOf('image/') === 0) {
          validFiles.push(f);
        }
      }
      if (validFiles.length === 0) return;

      var emptyInputs = getEmptyFileInputs();
      var needed = validFiles.length - emptyInputs.length;

      for (var j = 0; j < needed; j++) {
        addLink.click();
      }

      setTimeout(function() {
        emptyInputs = getEmptyFileInputs();
        for (var k = 0; k < validFiles.length && k < emptyInputs.length; k++) {
          assignFileToInput(emptyInputs[k], validFiles[k]);
        }
      }, 50);
    }

    dropzone.addEventListener('click', function() {
      var firstEmpty = getEmptyFileInputs()[0];
      if (firstEmpty) {
        firstEmpty.click();
      } else {
        addLink.click();
        setTimeout(function() {
          var empty = getEmptyFileInputs()[0];
          if (empty) empty.click();
        }, 50);
      }
    });

    dropzone.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('drag-over');
      e.dataTransfer.dropEffect = 'copy';
    });

    dropzone.addEventListener('dragleave', function(e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('drag-over');
    });

    dropzone.addEventListener('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('drag-over');
      if (e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
      }
    });

    dropzone.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        dropzone.click();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPropertyImageDropzone);
  } else {
    initPropertyImageDropzone();
  }
})();
