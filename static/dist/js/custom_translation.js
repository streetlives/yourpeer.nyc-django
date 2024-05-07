/*
Copyright (c) 2024 Streetlives, Inc.

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
*/

function initCustomTranslations() {
    if (window._hadCustomTranslationsInit) {
        return;
    }
    window.customTranslations = {
        es: {
            "Free support services validated by your peers": "Servicios de apoyo gratuito para personas en necesidad",
            "Home": "Inicio"
        },
        "zh-CN": {
            "Free support services validated by your peers": "经同行验证的免费支持服务",
            "Home": "家"
        },
        "bn": {
            "Free support services validated by your peers": "আপনার সহকর্মীদের দ্বারা যাচাইকৃত বিনামূল্যের সহায়তা পরিষেবা",
            "Home": "হোম"
        },
        "fr": {
            "Free support services validated by your peers": "Des services d'assistance gratuits validés par vos pairs",
            "Home": "maison"
        }
    };


    window.updateTranslations = function (current_lang) {
        const allElements = document.querySelectorAll('.customTranslation');
        allElements.forEach(element => {
            const text = element.dataset.text.trim();
            const currentLanguage = current_lang || 'en';
            if (customTranslations[currentLanguage] && customTranslations[currentLanguage][text]) {
                element.textContent = customTranslations[currentLanguage][text];
            } else {
                element.textContent = text;
            }
        });
    }
}
initCustomTranslations();
