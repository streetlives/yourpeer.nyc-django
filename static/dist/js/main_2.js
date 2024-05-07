/*
Copyright (c) 2024 Streetlives, Inc.

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
*/

let menuButton = document.getElementById('offCanvasMenuButton')
let offCanvasMenu = document.getElementById('offCanvasMenu')
let closeMenuButton = document.getElementById('closeMenu')
let menuOverlay = document.getElementById('menuOverlay')

function closeMenu(e) {
  offCanvasMenu.classList.remove('off-canvas-menu-active');
  console.log('close')
}

document.addEventListener("DOMContentLoaded", function () {
  // Filters Popup
  const allFilterButton = document.getElementById("allFiltersButton");
  const filtersPopup = document.getElementById("filtersPopup");
  const filtersCloseButton = document.getElementById("filtersPopupCloseButton");

  if (allFilterButton) {
    allFilterButton.addEventListener("click", openFiltersPopup);
    filtersCloseButton.addEventListener("click", closeFiltersPopup);
  }

  function openFiltersPopup() {
    filtersPopup.style.display = "flex";
  }

  function closeFiltersPopup() {
    filtersPopup.style.display = "none";
  }




    // offcanvas menu


    if (menuButton) {
      menuButton.addEventListener('click', function(e) {
        offCanvasMenu.classList.add('off-canvas-menu-active')
      })
    }
    
    if(closeMenuButton) {
      closeMenuButton.addEventListener('click', closeMenu)
      menuOverlay.addEventListener('click', closeMenu)
    }
    



    // when window scroll add background in navbar
    let navbar = document.getElementById('header')

    window.addEventListener('scroll', e => {
      let scrollPosition = window.scrollY;

      // Check if the scroll position is greater than or equal to 50px
      if (scrollPosition >= 50) {
        navbar.classList.add('bg-amber-300');
      } else {
        navbar.classList.remove('bg-amber-300');
      }
    });



});


