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
]

LABEL_RECEPTION_COMMUNAUTAIRE_OUI_SELECTORS = [
    "label[for='receptionCommunautaire_1']",
]

INPUT_TAUX_CO2_SAISI_SELECTORS = [
    "input#TauxCO2Saisi",
]

LABEL_VEHICULE_8PLACES_NON_SELECTORS = [
    "label[for='vehicule_8Places_2']",
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
]

SELECT_DEPARTEMENT_SELECTORS = [
    "select#departement",                                 # id 唯一，首选
]

BUTTON_RESULT_SELECTORS = [
    "button#btn_g6k_",
    "button.fr-btn#btn_g6k_",
    "button[name='result']"
]

COUT_CERTIFICAT_SELECTORS = [
    "div#Résultat-panel-1-blockinfo-4-chapter-1-section-1-content p.sp-blue strong",
    "div.section-content p.sp-blue strong",
]

LABEL_AUTONOMIE_50KM_OUI_SELECTORS = [
    "label[for='Autonomie50Km_1']"
]