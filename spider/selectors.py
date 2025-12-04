COOKIE_CONSENT_BUTTONS = [
    "button[title*='Accepter']",
    "button:has-text('Accepter')",
    "button.orejime-Notice-saveButton",
    "button[class*='save']",
    "button[type='button']:has-text('Accepter')"
]

LABEL_FRANCE_IMPORT_SELECTORS = [
    "label[for='franceOuImport_2']",
    "label.fr-label[for='franceOuImport_2']",
    "label:has-text('Importé en France après avoir été immatriculé dans un autre pays')",
]

SELECT_DEMARCHE_SELECTORS = [
    "select#demarche",
    "select.fr-select[name='demarche']",
    "select.form-control[name='demarche']",
    "select[aria-describedby='error-demarche']",
    "select[data-fr-js-select-actionee='true']"
]

SELECT_TYPE_VEHICULE_SELECTORS = [
    "select#typeVehicule",
    "select.fr-select[name='typeVehicule']",
    "select.form-control[name='typeVehicule']",
    "select[aria-describedby='error-typeVehicule']",
    "select[data-fr-js-select-actionee='true'][name='typeVehicule']"
]

INPUT_DATE_MISE_EN_CIRCULATION_SELECTORS = [
    "input#dateMiseEnCirculation",
    "input.fr-input[name='dateMiseEnCirculation']",
    "input[type='date'][name='dateMiseEnCirculation']",
    "input[aria-describedby='error-dateMiseEnCirculation']",
]

INPUT_PUISSANCE_ADM_SAISIE_SELECTORS = [
    "input#PuissanceAdmSaisie",
    "input.fr-input[name='PuissanceAdmSaisie']",
    "input[type='number'][name='PuissanceAdmSaisie']",
    "input[aria-describedby='error-PuissanceAdmSaisie']",
]

SELECT_ENERGIE_SELECTORS = [
    "select#energie",
    "select.fr-select[name='energie']",
    "select.form-control[name='energie']",
    "select[aria-describedby='error-energie']",
    "select[data-fr-js-select-actionee='true'][name='energie']"
]

LABEL_INVALIDITE_NON_SELECTORS = [
    "label[for='invalidite_2']",
    "label.fr-label[for='invalidite_2']",
    "label:has-text('Non')",
]

LABEL_RECEPTION_COMMUNAUTAIRE_OUI_SELECTORS = [
    "label[for='receptionCommunautaire_1']",
    "label.fr-label[for='receptionCommunautaire_1']",
    "label:has-text('Oui')",
]

INPUT_TAUX_CO2_SAISI_SELECTORS = [
    "input#TauxCO2Saisi",
    "input.fr-input[name='TauxCO2Saisi']",
    "input[type='number'][name='TauxCO2Saisi']",
    "input[aria-describedby='error-TauxCO2Saisi']",
]

LABEL_VEHICULE_8PLACES_NON_SELECTORS = [
    "label[for='vehicule_8Places_2']",
    "label.fr-label[for='vehicule_8Places_2']",
    "label:has-text('Non')",
]

LABEL_PERSON_MORALE_LOCATION_NON_SELECTORS = [
    "label[for='PersonMoraleLocation_2']",
    "label.fr-label[for='PersonMoraleLocation_2']",
    "label:has-text('Non')",
]

LABEL_PERSONNE_MORALE_NON_SELECTORS = [
    "label[for='personneMorale_2']",                # for 属性唯一，首选
    "label.fr-label[for='personneMorale_2']",       # class + for 联合，保险
    "label:has-text('Non')",                        # 文本兜底（页面唯一"Non"时安全）
]

INPUT_POIDS_SAISI_SELECTORS = [
    "input#poidsSaisi",                               # id 唯一，首选
    "input.fr-input[name='poidsSaisi']",              # class+name 联合，极稳
    "input[type='number'][name='poidsSaisi']",        # 类型+name，兜底
    "input[aria-describedby='error-poidsSaisi']",     # aria 属性兜底
]

SELECT_DEPARTEMENT_SELECTORS = [
    "select#departement",                                 # id 唯一，首选
    "select.fr-select[name='departement']",               # class + name 联合
    "select.form-control[name='departement']",            # 另一种 class + name 联合
    "select[aria-describedby='error-departement']",       # aria 属性兜底
    "select[data-fr-js-select-actionee='true'][name='departement']", # data-* 属性 + name
]

BUTTON_RESULT_SELECTORS = [
    "button#btn_g6k_",
    "button.fr-btn#btn_g6k_",
    "button[name='result']",                    # name 属性，兜底
    "button[data-fr-js-button-actionee='true']",# data 属性，部分页面专用
    "button[type='submit'][id='btn_g6k_']",     # type+id 联合
    "button.fr-btn[type='submit'][name='result']", # class+type+name
    "button:has-text('Résultat')",              # 文本兜底（适合 Playwright/BS4 >=4.12/jQuery）
]

COUT_CERTIFICAT_SELECTORS = [
    "div#Résultat-panel-1-blockinfo-4-chapter-1-section-1-content p.sp-blue strong",
    "div.section-content p.sp-blue strong",
    "div.section-content strong",
    "p.sp-blue strong",
]

LABEL_AUTONOMIE_50KM_OUI_SELECTORS = [
    "label[for='Autonomie50Km_1']",
    "div.fr-radio-group.fr-radio-rich label.fr-label",
    "input#Autonomie50Km_1 + label",
    "input[name='Autonomie50Km'][value='Oui'] + label",
]