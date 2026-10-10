"""
backend/disease_knowledge.py
============================
Curated agricultural knowledge database for all 38 PlantVillage disease classes.
Provides verified disease taxonomy, symptoms, favoring environmental conditions,
practical immediate steps, treatment protocols, prevention/sanitation, and precautions.
"""

from typing import Dict, Any, List, Optional


DISEASE_DATABASE: Dict[str, Dict[str, Any]] = {
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Olive-green to black velvety spots on leaf surface and fruit",
            "Leaves may become distorted, yellow, and drop prematurely",
            "Scabby, corky brown lesions developing on apple skin"
        ],
        "favoring_conditions": "Cool (15-24°C), wet, humid spring weather with prolonged leaf wetness (6+ hours).",
        "immediate_actions": [
            "Rake and remove or compost fallen leaves beneath the tree canopy to interrupt spore cycles.",
            "Prune congested interior branches to increase sunlight penetration and air movement.",
            "Avoid overhead irrigation that wets the foliar canopy."
        ],
        "treatment": [
            "Apply captan, mancozeb, or myclobutanil early in the green-tip or pink-bud stage.",
            "For organic orchards, use liquid copper or sulfur sprays following label instructions before rainfall.",
            "Rotate chemical fungicide modes of action (FRAC codes) to avoid pathogen resistance."
        ],
        "prevention": [
            "Plant resistant apple cultivars (e.g., Liberty, Prima, Freedom, Enterprise).",
            "Mow fallen leaves in autumn and apply 5% urea spray to accelerate leaf decomposition.",
            "Maintain 3-4 meter tree spacing for optimal canopy airflow."
        ],
        "precautions": "Follow label pre-harvest intervals (PHI). Avoid sulfur applications when temperatures exceed 30°C to prevent phytotoxicity."
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black Rot (Frogeye Leaf Spot)",
        "scientific_name": "Botryosphaeria obtusa",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Small circular purple spots on leaves expanding into 'frogeye' lesions with tan centers",
            "Firm brown rot on fruit with concentric dark rings, eventually mummifying",
            "Cankers forming on limbs and branches"
        ],
        "favoring_conditions": "Warm temperatures (20-27°C) with frequent rain; overwintering in mummified fruit and dead wood.",
        "immediate_actions": [
            "Prune out dead wood, fire blight strikes, and cankers 15 cm below visible infection.",
            "Remove and destroy all mummified apples hanging on branches or on the ground.",
            "Sanitize pruning tools with 70% isopropyl alcohol between cuts."
        ],
        "treatment": [
            "Apply protective fungicides (captan or thiophanate-methyl) from petal fall through cover sprays.",
            "Copper sprays applied during delayed dormant stage reduce initial inoculum.",
            "Ensure complete coverage of fruit clusters and upper canopies."
        ],
        "prevention": [
            "Keep trees vigorous through balanced fertilization; avoid excess nitrogen.",
            "Control insect wounds that provide entry sites for fungal spores.",
            "Promptly dispose of pruned wood away from the orchard perimeter."
        ],
        "precautions": "Wear personal protective equipment (PPE) when applying fungicides. Do not apply near water bodies."
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar Apple Rust",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "pathogen_type": "Fungal (Heteroecious)",
        "is_healthy": False,
        "severity_baseline": "Low to Moderate",
        "symptoms": [
            "Bright orange-yellow circular spots on upper leaf surfaces",
            "Tiny black pycnia dots in center of spots",
            "Raised tube-like aecia structures on leaf undersides shedding powdery spores"
        ],
        "favoring_conditions": "Presence of alternate hosts (Eastern red cedar/juniper); warm (12-24°C) wet spring weather.",
        "immediate_actions": [
            "Inspect nearby cedar or juniper trees within 1 km for galls (cedar apples) and prune them.",
            "Rake fallen leaves to maintain orchard sanitation.",
            "Monitor susceptible trees closely during early leaf emergence."
        ],
        "treatment": [
            "Apply myclobutanil, fenbuconazole, or propiconazole at pink bud stage through petal fall.",
            "Protective sprays with mancozeb provide control when timed before forecasted rainfall.",
            "Fungicide sprays are only effective if applied before symptoms appear."
        ],
        "prevention": [
            "Select rust-resistant apple varieties (e.g., Redfree, Liberty, Freedom, Arkansas Black).",
            "Eradicate wild red cedars within 300 to 500 meters of the orchard if feasible.",
            "Space trees to maximize sunlight and rapid leaf drying."
        ],
        "precautions": "Treatments applied after orange spots appear on apple leaves cannot cure current lesions."
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Foliage",
        "scientific_name": "Malus domestica",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Vibrant green leaves, crisp margins, no chlorosis, lesions, or spotting."],
        "favoring_conditions": "Balanced soil moisture, good drainage, full sun (6-8 hours daily), optimal pruning.",
        "immediate_actions": [
            "Maintain regular scouting routine every 7 to 10 days.",
            "Continue seasonal maintenance and soil moisture monitoring."
        ],
        "treatment": [
            "No chemical intervention needed.",
            "Maintain balanced fertility with N-P-K based on annual soil tests."
        ],
        "prevention": [
            "Apply dormant horticultural oil in late winter for scale and mite prevention.",
            "Mulch base (keep mulch 10 cm away from trunk) to retain soil moisture.",
            "Practice annual dormant pruning."
        ],
        "precautions": "Avoid unnecessary chemical applications to preserve beneficial predatory insects."
    },
    "Blueberry___healthy": {
        "crop": "Blueberry",
        "condition": "Healthy Foliage",
        "scientific_name": "Vaccinium corymbosum",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Uniformly green waxy leaves, vigorous shoots, no leaf discoloration or dieback."],
        "favoring_conditions": "Acidic soil (pH 4.5 - 5.5), well-drained organic matter, consistent shallow moisture.",
        "immediate_actions": ["Maintain soil pH monitoring and keep pine bark or peat mulch replenished."],
        "treatment": ["No fungicide or pesticide needed."],
        "prevention": [
            "Irrigate with drip systems at root zone; avoid foliar wetting.",
            "Test soil pH annually and amend with elemental sulfur if pH rises above 5.2.",
            "Prune oldest canes (>4 years) annually during dormancy."
        ],
        "precautions": "Avoid nitrate forms of nitrogen; use ammonium sulfate or organic acidic feeds."
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry",
        "condition": "Powdery Mildew",
        "scientific_name": "Podosphaera clandestina",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "White to light-gray powdery fungal growth on leaves and green shoots",
            "Leaves curl upwards, blister, and exhibit stunted deformed growth",
            "Fruit may develop circular whitish lesions and fail to ripen"
        ],
        "favoring_conditions": "Warm (18-28°C), shaded, humid canopies; does not require free water to infect.",
        "immediate_actions": [
            "Prune infected shoot tips ('flags') and destroy them.",
            "Improve canopy ventilation through selective summer pruning.",
            "Ensure overhead irrigation is avoided."
        ],
        "treatment": [
            "Apply potassium bicarbonate, horticultural oil, or sulfur at first sign of powdery patches.",
            "For severe outbreaks, use FRAC group 3 (myclobutanil) or group 11 (trifloxystrobin) fungicides.",
            "Ensure thorough underleaf spray coverage."
        ],
        "prevention": [
            "Ensure generous tree spacing and open-center canopy architecture.",
            "Avoid high nitrogen applications that stimulate tender, susceptible new flush.",
            "Scout weekly during warm spring and early summer periods."
        ],
        "precautions": "Never apply sulfur within 14-21 days of horticultural oils to prevent severe leaf burn."
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry",
        "condition": "Healthy Foliage",
        "scientific_name": "Prunus cerasus / Prunus avium",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Smooth, deep green leaves with glossy texture and healthy serrated margins."],
        "favoring_conditions": "Full sun, deep well-drained loamy soil, adequate winter chill hours.",
        "immediate_actions": ["Continue routine orchard maintenance."],
        "treatment": ["No treatment required."],
        "prevention": [
            "Dormant copper sprays in late autumn reduce bacterial canker risk.",
            "Paint lower trunks with white latex paint to prevent winter sunscald."
        ],
        "precautions": "Protect ripening fruit with bird netting."
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)",
        "condition": "Gray Leaf Spot",
        "scientific_name": "Cercospora zeae-maydis",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Rectangular lesions delimited by leaf veins with sharp parallel borders",
            "Lesions start tan and turn grayish as fungal spores mature",
            "Extensive blighting causing premature canopy death and lodging"
        ],
        "favoring_conditions": "Warm (24-30°C), high relative humidity (>90%), extended morning dew or fog.",
        "immediate_actions": [
            "Scout lower leaves prior to tasseling (V14 to R1 growth stages).",
            "Determine if lesion thresholds justify economic fungicide return on susceptible hybrids.",
            "Minimize irrigation duration during overcast days."
        ],
        "treatment": [
            "Apply strobilurin (QoI) + triazole (DMI) combination fungicides at VT-R1 (tassel to silking).",
            "Ensure adequate spray volume (15-20 gal/acre ground, 5 gal/acre aerial) for canopy penetration."
        ],
        "prevention": [
            "Plant corn hybrids with high Gray Leaf Spot resistance scores.",
            "Rotate fields with non-host crops (soybeans, alfalfa, small grains) for at least 1-2 years.",
            "Tillage to bury infested corn stubble if erosion constraints permit."
        ],
        "precautions": "Do not apply fungicides with adjuvants between V8 and VT to prevent arrested ear development."
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "condition": "Common Rust",
        "scientific_name": "Puccinia sorghi",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Oval to elongated cinnamon-brown pustules scattered across both leaf surfaces",
            "Pustules rupture epidermal tissue releasing reddish-brown powdery urediniospores",
            "Pustules turn dark brownish-black late in the season (teliospore stage)"
        ],
        "favoring_conditions": "Moderate temperatures (16-24°C) and high humidity (near 100%), dew periods.",
        "immediate_actions": [
            "Scout fields during whorl and tasseling stages.",
            "Distinguish from Southern Rust (Southern rust has smaller orange pustules mainly on upper leaf)."
        ],
        "treatment": [
            "Apply foliar fungicides (pyraclostrobin, azoxystrobin + propiconazole) if rust appears before silking on susceptible inbreds/hybrids.",
            "Usually economic only in seed production or sweet corn fields."
        ],
        "prevention": [
            "Plant commercially available resistant hybrids with Rp gene resistance.",
            "Plant early in the season to avoid late-season airborne spore showers from southern regions."
        ],
        "precautions": "Follow restricted entry intervals (REI) indicated on product labels."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "condition": "Northern Corn Leaf Blight",
        "scientific_name": "Exserohilum turcicum",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Severe",
        "symptoms": [
            "Long, cigar-shaped, elliptical grayish-green or tan lesions (2.5 to 15 cm long)",
            "Dark olive-green velvety spores produced inside lesions during damp weather",
            "Lesions coalesce, killing large portions of the photosynthetic leaf area"
        ],
        "favoring_conditions": "Moderate temperatures (18-27°C) accompanied by heavy dews and frequent rainfall.",
        "immediate_actions": [
            "Assess disease severity on the ear leaf and leaves immediately above it around silking.",
            "If lesions are present on 50% of plants before tasseling on susceptible hybrids, prepare fungicide application."
        ],
        "treatment": [
            "Apply premix fungicides containing triazole + strobilurin (e.g., fluxapyroxad + pyraclostrobin).",
            "Optimal application window is VT to R2."
        ],
        "prevention": [
            "Select hybrids with single-gene (Ht) or polygenic resistance.",
            "Rotate with non-grass crops for at least two seasons.",
            "Incorporate residue to accelerate microbial breakdown of overwintering chlamydospores."
        ],
        "precautions": "Respect the pre-harvest interval for grain vs. silage harvesting."
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "condition": "Healthy Foliage",
        "scientific_name": "Zea mays",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Uniform green, arching strap-like leaves with intact venation and no pustules or blights."],
        "favoring_conditions": "Full sun, adequate nitrogen, 50-60 cm annual moisture, warm growing degree days.",
        "immediate_actions": ["Conduct routine weekly crop scouting."],
        "treatment": ["No fungicide needed. Maintain side-dress nitrogen schedule."],
        "prevention": [
            "Practice continuous weed control to prevent microclimate moisture stagnation.",
            "Maintain balanced fertility with starter and side-dress nutrient applications."
        ],
        "precautions": "Ensure planter calibration for uniform emergence."
    },
    "Grape___Black_rot": {
        "crop": "Grape",
        "condition": "Black Rot",
        "scientific_name": "Guignardia bidwellii",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Severe",
        "symptoms": [
            "Circular reddish-brown leaf spots with dark borders and tiny black pycnidia pimples",
            "Berries develop light brown spots, soften, shrivel into hard black wrinkled mummies",
            "Black elliptical cankers on young shoots"
        ],
        "favoring_conditions": "Warm (21-27°C) wet weather with 6-24 hours of continuous leaf/berry moisture.",
        "immediate_actions": [
            "Prune out mummified berries and infected canes during dormant pruning; burn or bury them.",
            "Tuck shoots into trellis wires to improve air circulation and sunlight drying."
        ],
        "treatment": [
            "Apply mancozeb, captan, or myclobutanil starting at 2.5 cm shoot growth through 4 weeks post-bloom.",
            "Critical window: immediate pre-bloom to 4 weeks after bloom when berries are highly vulnerable."
        ],
        "prevention": [
            "Select resistant or moderately resistant cultivars.",
            "Keep canopy open with leaf pulling around fruit zones in cool climates.",
            "Maintain clean vineyard floor under vine rows."
        ],
        "precautions": "Do not apply mancozeb within 66 days of grape harvest."
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "condition": "Esca (Black Measles)",
        "scientific_name": "Phaeomoniella chlamydospora & Phaeoacremonium minimum",
        "pathogen_type": "Fungal Complex (Wood-decay)",
        "is_healthy": False,
        "severity_baseline": "Severe",
        "symptoms": [
            "'Tiger-stripe' chlorotic and necrotic interveinal patterns on leaves",
            "Berries develop speckled dark purple/brown spots ('measles') and crack",
            "Sudden vine apoplexy (complete vine collapse) during hot dry spells; spongy wood rot inside trunk"
        ],
        "favoring_conditions": "Mature vineyards (>8 years); stress from high heat and drought following wet springs.",
        "immediate_actions": [
            "Mark symptomatic vines in summer for separate dormant pruning.",
            "Prune symptomatic cordons back to healthy white wood.",
            "Do not prune during wet rainy periods when spores are airborne."
        ],
        "treatment": [
            "No curative chemical fungicide can eradicate fungal pathogens inside the trunk wood.",
            "Apply wound protectants (e.g., thiophanate-methyl, boron paste, or Trichoderma biocontrol) to pruning cuts."
        ],
        "prevention": [
            "Adopt double pruning or delayed late-winter pruning when wound healing is rapid.",
            "Minimize large pruning wounds; disinfect pruning shears between vines.",
            "Retrain a healthy sucker from the base if trunk must be replaced."
        ],
        "precautions": "Discard infected cordons away from vineyard; do not leave dead vine wood in the row middles."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "condition": "Leaf Blight (Isariopsis Leaf Spot)",
        "scientific_name": "Pseudocercospora vitis (Isariopsis clavispora)",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Large, irregular reddish-brown necrotic spots with distinct dark brown margins",
            "Lesions coalesce, causing premature leaf drying and defoliation late in the season",
            "Dark olive-colored moldy growth visible on underside of spots in high humidity"
        ],
        "favoring_conditions": "Warm, humid climates, especially late summer and early autumn.",
        "immediate_actions": [
            "Remove heavily spotted leaves if defoliation is beginning.",
            "Maintain good canopy canopy openness."
        ],
        "treatment": [
            "Copper hydroxide or mancozeb sprays provide effective protective control.",
            "Strobilurin fungicides (e.g., azoxystrobin) effective in conventional management programs."
        ],
        "prevention": [
            "Post-harvest copper spray to protect canopy until natural dormancy.",
            "Canopy management: shoot positioning and lateral removal."
        ],
        "precautions": "Avoid copper phytotoxicity on copper-sensitive cultivars in cool, humid conditions."
    },
    "Grape___healthy": {
        "crop": "Grape",
        "condition": "Healthy Foliage",
        "scientific_name": "Vitis vinifera / Vitis labrusca",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Vigorous green palmate leaves with intact lobes, clean margins, and healthy tendril development."],
        "favoring_conditions": "Full sunlight, well-draining sloping soil, balanced canopy shoot density (15 shoots/meter).",
        "immediate_actions": ["Maintain shoot positioning and regular vineyard scouting."],
        "treatment": ["No fungicide needed."],
        "prevention": [
            "Maintain weed-free vine strip.",
            "Implement preventative canopy management (shoot thinning, suckering)."
        ],
        "precautions": "Monitor soil moisture to prevent water stress during veraison."
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange (Citrus)",
        "condition": "Huanglongbing (Citrus Greening)",
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "pathogen_type": "Bacterial (Vector: Asian Citrus Psyllid)",
        "is_healthy": False,
        "severity_baseline": "Severe (Fatal to tree)",
        "symptoms": [
            "Asymmetrical, blotchy mottled yellowing across leaf blades (crossing the main veins)",
            "Thickened, corky, upright leaves with zinc/iron deficiency-like yellowing",
            "Small, lopsided, bitter fruit that stays green at the blossom end; twig dieback"
        ],
        "favoring_conditions": "Presence of the Asian Citrus Psyllid (Diaphorina citri); warm subtropical climates.",
        "immediate_actions": [
            "Quarantine and report suspected cases to local agricultural extension immediately.",
            "Scout for Asian Citrus Psyllid nymphs and adults on new feather flush.",
            "Confirmed positive trees must be removed to protect neighboring citrus groves."
        ],
        "treatment": [
            "No cure exists for infected trees; disease is systemic and fatal.",
            "Aggressive psyllid control: systemic insecticides (imidacloprid, thiamethoxam) or foliar sprays.",
            "Nutritional foliar sprays may prolong productivity temporarily but do not cure infection."
        ],
        "prevention": [
            "Plant only certified disease-free nursery stock from insect-proof greenhouses.",
            "Release biological control agents (Tamarixia radiata parasitoid wasp).",
            "Strictly observe regional citrus quarantine zones; do not transport citrus plant material."
        ],
        "precautions": "Follow regulatory quarantine mandates in citrus-producing jurisdictions."
    },
    "Peach___Bacterial_spot": {
        "crop": "Peach",
        "condition": "Bacterial Spot",
        "scientific_name": "Xanthomonas arboricola pv. pruni",
        "pathogen_type": "Bacterial",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Water-soaked angular purple-brown spots on leaves that dry and drop out ('shot-hole' effect)",
            "Severe yellowing of leaves around lesions leading to heavy early defoliation",
            "Pitted, cracked, gummy lesions on peach fruit skins"
        ],
        "favoring_conditions": "Warm (21-30°C), windy, rainy conditions; blowing sandy soils causing micro-abrasions.",
        "immediate_actions": [
            "Avoid overhead irrigation.",
            "Prune during dry sunny weather only; sanitize shears between trees.",
            "Do not over-fertilize with nitrogen, which produces highly susceptible tender growth."
        ],
        "treatment": [
            "Apply low-rate copper hydroxide or oxytetracycline starting from shuck split through cover sprays.",
            "Dormant copper sprays at bud swell help reduce overwintering bacterial population."
        ],
        "prevention": [
            "Plant resistant peach varieties (e.g., Clayton, Candor, Biscoe, Harrow Beauty).",
            "Establish windbreaks in sandy soil regions to minimize wind-blown sand abrasion.",
            "Prune trees to open vase architecture for fast foliar drying."
        ],
        "precautions": "Be cautious with copper rates post-bloom on peaches; excessive copper causes severe leaf burn and defoliation."
    },
    "Peach___healthy": {
        "crop": "Peach",
        "condition": "Healthy Foliage",
        "scientific_name": "Prunus persica",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Lush, lanceolate dark green leaves with clean margins and no shot-hole spotting."],
        "favoring_conditions": "Full sun, deep well-drained sandy loam soil, proper winter pruning.",
        "immediate_actions": ["Continue routine orchard management."],
        "treatment": ["No treatment required."],
        "prevention": [
            "Dormant spray of copper or chlorothalonil in late autumn/early spring for peach leaf curl prevention.",
            "Maintain mulch ring and drip irrigation."
        ],
        "precautions": "Thin fruit clusters in spring to prevent branch breakage and fruit rot."
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Pepper (Bell)",
        "condition": "Bacterial Spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "pathogen_type": "Bacterial",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Small, water-soaked, circular to irregular dark spots on leaves becoming necrotic with yellow halos",
            "Underleaf lesions may have slightly raised, blister-like centers",
            "Severe leaf drop exposing fruit to sunscald; rough, raised warty scabs on fruit"
        ],
        "favoring_conditions": "Warm (24-30°C), high relative humidity, splashing rain or overhead irrigation.",
        "immediate_actions": [
            "Do not handle, prune, or harvest plants when foliage is wet.",
            "Remove and destroy severely infected individual plants.",
            "Shift to drip irrigation at base of plants immediately."
        ],
        "treatment": [
            "Apply copper bactericide combined with mancozeb (co-application increases free copper ions).",
            "Apply Actigard (acibenzolar-S-methyl) plant defense inducer early in the season.",
            "Bacillus subtilis biological bactericides can be used in organic rotations."
        ],
        "prevention": [
            "Use certified pathogen-free, hot-water-treated seeds.",
            "Select resistant bell pepper hybrids with multiple race resistance (Xcv 1-10).",
            "Rotate crops for at least 2-3 years away from solanaceous crops (tomatoes, peppers, potatoes)."
        ],
        "precautions": "Copper-resistant bacterial strains exist; avoid continuous solitary copper applications."
    },
    "Pepper,_bell___healthy": {
        "crop": "Pepper (Bell)",
        "condition": "Healthy Foliage",
        "scientific_name": "Capsicum annuum",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Firm, glossy deep green leaves with crisp margins and vigorous branching."],
        "favoring_conditions": "Warm soil, consistent watering, full sunlight, balanced magnesium and calcium.",
        "immediate_actions": ["Maintain drip irrigation and weekly pest scouting."],
        "treatment": ["No chemical treatment required."],
        "prevention": [
            "Stake or cage plants to keep foliage elevated off soil.",
            "Apply organic mulch around root zones."
        ],
        "precautions": "Avoid high nitrogen levels that promote excessive foliage at the expense of fruit set."
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early Blight",
        "scientific_name": "Alternaria solani",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Dark brown to black circular lesions on older lower foliage with concentric rings ('target board')",
            "Yellowing (chlorosis) halo surrounding lesions",
            "Infected leaves eventually wither, dry out, and drop prematurely"
        ],
        "favoring_conditions": "Warm temperatures (24-29°C) with alternating wet periods and dry windy spells.",
        "immediate_actions": [
            "Remove and destroy heavily blighted lower leaves.",
            "Ensure plants are adequately irrigated; drought stress accelerates early blight susceptibility.",
            "Sanitize boots and equipment between field plots."
        ],
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin preventative fungicides on a 7-10 day schedule.",
            "Copper fungicides provide protective suppression in organic cultivation.",
            "Ensure complete coverage of lower canopy leaves."
        ],
        "prevention": [
            "Plant certified disease-free seed tubers.",
            "Maintain 3-year crop rotation avoiding other nightshades (tomato, eggplant, pepper).",
            "Ensure adequate nitrogen and potassium fertilization; under-fertilized crops are highly vulnerable."
        ],
        "precautions": "Rotate fungicide FRAC codes (e.g., FRAC 3, 7, 9, 11) to avoid fungicide resistance."
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "pathogen_type": "Oomycete (Water Mold)",
        "is_healthy": False,
        "severity_baseline": "Severe (High Emergency)",
        "symptoms": [
            "Large, irregular, water-soaked dark greenish-brown lesions expanding rapidly across foliage",
            "Fine white cottony/powdery mildew growth visible on leaf undersides in moist weather",
            "Rapid collapse of entire canopy ('blighted' appearance with foul rotting odor); firm brown tuber rot"
        ],
        "favoring_conditions": "Cool to moderate temperatures (15-22°C) and sustained high humidity (>90%) with rain/dew.",
        "immediate_actions": [
            "Immediately destroy infected plant tissue; do not compost blighted haulms.",
            "Alert neighboring growers and local agricultural extension; late blight spreads exponentially by wind.",
            "Kill vines (flail or desiccant) 2 weeks before harvest if late blight is active to protect tubers."
        ],
        "treatment": [
            "Apply systemic late-blight fungicides: mandipropamid, cyazofamid, fluopicolide, or metalaxyl/mefenoxam.",
            "For organic systems, apply fixed copper before rain events (preventative only)."
        ],
        "prevention": [
            "Plant certified disease-free seed potatoes; eliminate cull piles in spring.",
            "Choose resistant varieties (e.g., Defiance, Sarpo Mira, Elba).",
            "Monitor regional Late Blight Decision Support Systems (DSS) / Blight Cast alerts."
        ],
        "precautions": "Late blight can destroy an entire field within 7-10 days if left untreated. Prompt action is mandatory."
    },
    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy Foliage",
        "scientific_name": "Solanum tuberosum",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Lush, compound green foliage with strong stems and uniform leaf texture."],
        "favoring_conditions": "Cool nights (15-18°C), loose well-drained acidic soil (pH 5.0-6.0), steady hilling.",
        "immediate_actions": ["Maintain hilling schedule and scout lower canopies twice weekly."],
        "treatment": ["No treatment required."],
        "prevention": [
            "Hill soil around plant bases to protect developing tubers from light and spore exposure.",
            "Maintain balanced N-P-K nutrition."
        ],
        "precautions": "Avoid waterlogging; saturated soil encourages soft rots and root suffocation."
    },
    "Raspberry___healthy": {
        "crop": "Raspberry",
        "condition": "Healthy Foliage",
        "scientific_name": "Rubus idaeus",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Pinnately compound bright green leaves, vigorous canes, no chlorosis or cane cankers."],
        "favoring_conditions": "Well-drained rich soil, full sun, trellis support, adequate row spacing.",
        "immediate_actions": ["Maintain weed management and trellis training."],
        "treatment": ["No treatment needed."],
        "prevention": [
            "Prune out spent floricanes immediately after fruiting.",
            "Keep cane density to 4-5 vigorous primocanes per foot of row."
        ],
        "precautions": "Do not plant in areas where verticillium-susceptible crops (tomatoes, potatoes) grew recently."
    },
    "Soybean___healthy": {
        "crop": "Soybean",
        "condition": "Healthy Foliage",
        "scientific_name": "Glycine max",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Trifoliate rich green leaves with clean surfaces, robust nodules on roots, sturdy stems."],
        "favoring_conditions": "Warm summer temperatures (20-30°C), adequate soil moisture during flowering (R1-R3).",
        "immediate_actions": ["Continue routine field scouting for defoliating insects."],
        "treatment": ["No fungicide needed."],
        "prevention": [
            "Rotate with corn, wheat, or grain sorghum.",
            "Use inoculant (Bradyrhizobium japonicum) on seed if planting in non-soybean history soil."
        ],
        "precautions": "Avoid soil compaction during planting operations."
    },
    "Squash___Powdery_mildew": {
        "crop": "Squash",
        "condition": "Powdery Mildew",
        "scientific_name": "Podosphaera xanthii (syn. Sphaerotheca fuliginea)",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Talcum-powder-like white fungal colonies on upper and lower leaf surfaces and petioles",
            "Infected leaves turn yellow, brown, and become brittle and paper-thin",
            "Premature defoliation leads to sunscald on ripening squash and reduced yields"
        ],
        "favoring_conditions": "Warm (20-27°C), dry air with dense shaded canopies; high humidity during night.",
        "immediate_actions": [
            "Prune older heavily infected lower leaves and discard.",
            "Ensure plants are not crowded; increase air movement between hills.",
            "Switch to drip irrigation."
        ],
        "treatment": [
            "Apply potassium bicarbonate, neem oil, or horticultural oil at earliest onset.",
            "Conventional fungicides: triflumizole, quinoxyfen, or myclobutanil; rotate FRAC groups.",
            "Biofungicides (e.g., Bacillus amyloliquefaciens) provide organic suppression."
        ],
        "prevention": [
            "Select squash varieties with genetic powdery mildew resistance (PMR).",
            "Maintain generous row and plant spacing (minimum 1-1.5 meters).",
            "Remove all cucurbit plant residues promptly at end of season."
        ],
        "precautions": "Do not apply horticultural oils when air temperatures exceed 32°C."
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "condition": "Leaf Scorch",
        "scientific_name": "Diplocarpon earlianum",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Numerous small, irregular purple-to-dark-brown blotches on upper leaf surfaces",
            "Spots lack white centers (distinguishing scorch from common leaf spot)",
            "Tissues between lesions dry, turn brown, and leaf margins curl upward with a burned appearance"
        ],
        "favoring_conditions": "Warm (20-26°C), wet conditions with long periods of free moisture on leaves.",
        "immediate_actions": [
            "Rake and remove old spotted leaves after harvest during bed renovation.",
            "Avoid sprinkler irrigation; use drip tapes under plastic mulch."
        ],
        "treatment": [
            "Apply captan, thiram, or pyraclostrobin during spring growth and pre-bloom.",
            "Copper sprays can be applied in late autumn or early spring."
        ],
        "prevention": [
            "Plant resistant strawberry cultivars (e.g., Allstar, Earliglow, Honeoye).",
            "Renovate matted-row plantings promptly after harvest (mow foliage, narrow rows).",
            "Keep beds weed-free to maximize air circulation and rapid foliage drying."
        ],
        "precautions": "Follow product labels for pre-harvest intervals during the active picking season."
    },
    "Strawberry___healthy": {
        "crop": "Strawberry",
        "condition": "Healthy Foliage",
        "scientific_name": "Fragaria × ananassa",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Trifoliate glossy green leaves with serrated margins, clean crowns, vigorous runners."],
        "favoring_conditions": "Full sun, rich sandy loam soil (pH 5.5-6.5), straw mulch, consistent moisture.",
        "immediate_actions": ["Maintain clean straw or plastic mulch beneath berries."],
        "treatment": ["No fungicide required."],
        "prevention": [
            "Mulch with clean straw over winter in freezing climates to protect crowns.",
            "Replace planting beds every 3-4 years to avoid buildup of soil-borne pathogens."
        ],
        "precautions": "Do not bury crowns too deeply when transplanting."
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "condition": "Bacterial Spot",
        "scientific_name": "Xanthomonas perforans / Xanthomonas vesicatoria",
        "pathogen_type": "Bacterial",
        "is_healthy": False,
        "severity_baseline": "Severe",
        "symptoms": [
            "Small (less than 3 mm), dark brown, water-soaked circular to angular spots on leaves",
            "Spots may have a faint yellow halo and appear greasy on leaf undersides",
            "Leaf centers often tear or drop out; small raised black scabs on green tomato fruit"
        ],
        "favoring_conditions": "Warm (24-30°C), wet, rainy weather; overhead irrigation and wind-driven rain.",
        "immediate_actions": [
            "Avoid working in tomato fields when leaves are wet to prevent spreading bacteria.",
            "Prune infected lower foliage with disinfected shears.",
            "Shift to drip irrigation at soil level immediately."
        ],
        "treatment": [
            "Apply fixed copper bactericides tank-mixed with mancozeb to overcome copper-tolerant strains.",
            "Apply acibenzolar-S-methyl (Actigard) systemic acquired resistance inducer.",
            "Use bacteriophage treatments (e.g., AgriPhage) for targeted biological suppression."
        ],
        "prevention": [
            "Use certified disease-free, hot-water-treated seed and transplants.",
            "Practice a 2- to 3-year crop rotation away from solanaceous plants.",
            "Eradicate nightshade weeds that serve as alternate bacterial reservoirs."
        ],
        "precautions": "Antibiotics (streptomycin) are not permitted on field tomatoes in most regions. Adhere to copper application limits."
    },
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early Blight",
        "scientific_name": "Alternaria solani / Alternaria linariae",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Dark brown to black concentric ring lesions ('target boards') on older lower leaves",
            "Progressive yellowing (chlorosis) of surrounding leaf tissue advancing upward",
            "Stem collar rot on young seedlings; dark sunken leathery lesions at stem end of fruit"
        ],
        "favoring_conditions": "Warm temperatures (24-29°C) with alternating periods of high humidity and rain with dry spells.",
        "immediate_actions": [
            "Prune and destroy all spotted lower foliage up to 30-40 cm from soil surface.",
            "Apply organic or plastic mulch around base to prevent soil splashback onto foliage.",
            "Stake or cage plants to maintain upright habit and good air penetration."
        ],
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin preventative fungicides on a 7-10 day cycle.",
            "For organic growers, spray copper octanoate or copper sulfate pentahydrate before rain.",
            "Ensure thorough under-leaf coverage throughout the lower and middle canopy."
        ],
        "prevention": [
            "Select tolerant or resistant cultivars (e.g., Mountain Supreme, Defiant PhR, Iron Lady).",
            "Practice a strict 3-year rotation avoiding peppers, eggplants, and potatoes.",
            "Drip-irrigate in the early morning; never use overhead sprinklers."
        ],
        "precautions": "Observe pre-harvest intervals (PHI). Rotate chemical classes (FRAC 3, 7, 9, 11) to avoid resistance."
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "pathogen_type": "Oomycete (Water Mold)",
        "is_healthy": False,
        "severity_baseline": "Severe (High Emergency)",
        "symptoms": [
            "Large, irregular, water-soaked pale green to dark brown lesions on leaves and stems",
            "Delicate white fungal-like sporulation visible on the underside of infected leaves in damp conditions",
            "Large, firm, greasy brown lesions on tomato fruits; rapid death of entire plant within days"
        ],
        "favoring_conditions": "Cool to moderate temperatures (15-22°C) with persistent high humidity (>90%) and rain or heavy fog.",
        "immediate_actions": [
            "Immediately bag and remove infected plants; do not compost blighted material.",
            "Check local extension alerts (USABlight / regional warning networks).",
            "Sanitize trellising stakes and tools with 10% bleach solution."
        ],
        "treatment": [
            "Apply specialized oomycete fungicides: cyazofamid, mandipropamid, fluopicolide, or mefenoxam.",
            "In organic farming, copper fungicides must be applied before infection as a protective shield."
        ],
        "prevention": [
            "Plant resistant tomato varieties (e.g., Defiant, Mountain Merit, Plum Regal, Iron Lady).",
            "Avoid planting adjacent to potato fields (both crops share this pathogen).",
            "Ensure maximum spacing (75-90 cm between plants) for rapid canopy drying."
        ],
        "precautions": "Spores can travel up to 15-30 km on wind currents. Late blight requires immediate aggressive action."
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "condition": "Leaf Mold",
        "scientific_name": "Passalora fulva (syn. Fulvia fulva, Cladosporium fulvum)",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Pale green to yellowish spots with indistinct margins on upper surface of older leaves",
            "Dense, velvety, olive-green to grayish-purple mold growth directly beneath spots on leaf undersides",
            "Leaves turn brown, curl, wither, and drop prematurely; rare fruit symptoms"
        ],
        "favoring_conditions": "High relative humidity (>85%) and warm temperatures (21-24°C); very common in greenhouses and high tunnels.",
        "immediate_actions": [
            "Open greenhouse ventilation fans, roll up sidewalls, and lower relative humidity below 80%.",
            "Prune infected lower foliage to increase air circulation inside the plant canopy.",
            "Eliminate overhead watering and maintain heated air circulation at night."
        ],
        "treatment": [
            "Apply preventative fungicides (chlorothalonil, mancozeb, or copper compounds).",
            "Biofungicides containing Bacillus subtilis or Trichoderma harzianum provide suppression.",
            "Ensure complete spray coverage of lower leaf surfaces."
        ],
        "prevention": [
            "Select tomato cultivars with Cf-gene resistance (e.g., many modern Dutch greenhouse hybrids).",
            "Space plants generously in greenhouse environments.",
            "Sanitize greenhouse structures and trellising between crop cycles."
        ],
        "precautions": "Fungicide efficacy is limited without environmental humidity control."
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "condition": "Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Numerous small (1.5 to 3 mm), circular spots with dark brown margins and sunken grayish-tan centers",
            "Tiny black specks (pycnidia fruiting bodies) visible in the center of lesions under magnification",
            "Progresses rapidly upward from lower leaves; leaves turn yellow, die, and drop off"
        ],
        "favoring_conditions": "Warm temperatures (20-25°C) and extended periods of wet weather with rain splashing.",
        "immediate_actions": [
            "Remove spotted lower leaves as soon as first spots appear on bottom branches.",
            "Apply a thick organic or plastic mulch barrier beneath the plants.",
            "Disinfect hands and tools after handling diseased plants."
        ],
        "treatment": [
            "Apply protective fungicides (chlorothalonil, mancozeb, or copper) every 7-10 days in wet seasons.",
            "Strobilurin fungicides (azoxystrobin) or FRAC 7/11 premixes can be used conventionally."
        ],
        "prevention": [
            "Practice a 3-year crop rotation away from solanaceous plants.",
            "Destroy all solanaceous crop debris and weeds (such as horsenettle) at season's end.",
            "Water exclusively with drip irrigation to avoid foliar wetting."
        ],
        "precautions": "Unlike early blight, Septoria spots are smaller, more numerous, and feature gray centers with black dots."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "condition": "Two-Spotted Spider Mites",
        "scientific_name": "Tetranychus urticae",
        "pathogen_type": "Arachnid Pest",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Fine pale yellow or white stippling (tiny dots) on the upper surface of leaves",
            "Leaves take on a bronze, dusty, or bleached appearance",
            "Fine silken webbing on leaf undersides, growing tips, and between stems; tiny moving mites visible"
        ],
        "favoring_conditions": "Hot (>28°C), dry, dusty conditions with low relative humidity.",
        "immediate_actions": [
            "Spray undersides of leaves with strong streams of water to disrupt webbing and dislodge mites.",
            "Prune heavily infested leaves and destroy them immediately.",
            "Avoid broad-spectrum synthetic insecticides (carbaryl, pyrethroids) that kill predatory mites."
        ],
        "treatment": [
            "Apply insecticidal soap or horticultural oil thoroughly to leaf undersides every 3-5 days.",
            "Release biological predatory mites (Phytoseiulus persimilis or Neoseiulus californicus).",
            "For severe commercial infestations, apply specific miticides (abamectin, bifenazate, spiromesifen)."
        ],
        "prevention": [
            "Keep paths and perimeters watered to minimize dust in greenhouses and garden plots.",
            "Maintain adequate plant watering to avoid drought-induced mite population spikes.",
            "Scout weekly with a 10x hand lens on the undersides of middle and upper canopy leaves."
        ],
        "precautions": "Miticides must be rotated frequently to prevent rapid resistance development."
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "condition": "Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "pathogen_type": "Fungal",
        "is_healthy": False,
        "severity_baseline": "Moderate",
        "symptoms": [
            "Brown circular lesions with faint concentric rings and light brown centers on leaves",
            "Lesions start as pinpoint brown spots and expand to 5-10 mm with yellow halos",
            "Sunken, crater-like brown lesions developing on green and ripe tomato fruit"
        ],
        "favoring_conditions": "Warm temperatures (20-30°C) with prolonged relative humidity (>80%) and rain.",
        "immediate_actions": [
            "Prune diseased lower leaves and maintain open canopy architecture.",
            "Avoid sprinkler irrigation."
        ],
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin + difenoconazole.",
            "Copper bactericide/fungicide tank mixes provide moderate suppression."
        ],
        "prevention": [
            "Maintain generous row and plant spacing for air circulation.",
            "Rotate crops with non-susceptible species for 2 years.",
            "Incorporate crop residues deeply after final harvest."
        ],
        "precautions": "Do not confuse with Early Blight (Target Spot fruit lesions are circular craters, not stem-end rots)."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Tomato yellow leaf curl virus (Begomovirus)",
        "pathogen_type": "Viral (Vector: Silverleaf Whitefly)",
        "is_healthy": False,
        "severity_baseline": "Severe (Stunts growth)",
        "symptoms": [
            "Severe upward curling and cupping of leaf margins",
            "Pronounced interveinal and marginal yellowing (chlorosis) of younger foliage",
            "Severe plant stunting, bushy upright habit, blossom drop, and near-complete failure to set fruit"
        ],
        "favoring_conditions": "High populations of Silverleaf Whitefly (Bemisia tabaci); warm climates year-round.",
        "immediate_actions": [
            "Carefully bag and rogue out infected plants immediately to prevent whitefly transmission.",
            "Install yellow sticky cards to monitor and suppress adult whitefly populations."
        ],
        "treatment": [
            "Viruses cannot be cured with chemical sprays once inside the plant.",
            "Direct all control measures toward the whitefly vector: insecticidal soaps, neem, or systemic neonicotinoids.",
            "Protect young transplants with physical insect-exclusion netting (50-mesh)."
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato hybrids (e.g., Tycoon, Skyway, Charger, Red Bounty).",
            "Use reflective silver mulches that repel whiteflies during early plant establishment.",
            "Maintain a 2-month host-free crop break in regional commercial production areas."
        ],
        "precautions": "Do not leave volunteer tomato plants or weed hosts (e.g., nightshades, mallows) near the field."
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "condition": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tomato mosaic virus (Tobamovirus)",
        "pathogen_type": "Viral (Mechanically Transmitted)",
        "is_healthy": False,
        "severity_baseline": "Moderate to Severe",
        "symptoms": [
            "Mottling of light and dark green patches on leaves ('mosaic' pattern)",
            "Leaves may become distorted, narrow, wrinkled, or fern-like ('shoestring' symptom)",
            "Internal brown browning ('brown wall') inside ripening fruit"
        ],
        "favoring_conditions": "Transmitted by human hands, pruning shears, contaminated tools, seed, and smoking/tobacco products.",
        "immediate_actions": [
            "Remove and incinerate infected plants immediately.",
            "Wash hands thoroughly with soap and water or skim milk before touching healthy tomatoes.",
            "Do not allow workers who use tobacco products to handle plants without decontamination."
        ],
        "treatment": [
            "No chemical cure exists for viral plant infections.",
            "Disinfect pruning shears, stakes, and flats with a 20% non-fat dry milk solution or 10% trisodium phosphate (TSP)."
        ],
        "prevention": [
            "Plant certified mosaic-resistant cultivars (designated with 'T' or 'ToMV' in seed catalogs).",
            "Use heat-treated or certified clean seed.",
            "Steam or sanitize propagation trays between seedings."
        ],
        "precautions": "Tobamoviruses are extremely stable and can persist on dry stakes, tools, and roots for years."
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy Foliage",
        "scientific_name": "Solanum lycopersicum",
        "pathogen_type": "None",
        "is_healthy": True,
        "severity_baseline": "None",
        "symptoms": ["Lush, deep green compound leaves with crisp serrated margins, sturdy stems, and no spotting."],
        "favoring_conditions": "Full sun (8+ hours), fertile well-drained soil (pH 6.2-6.8), consistent soil moisture, adequate calcium.",
        "immediate_actions": [
            "Maintain weekly scouting of lower leaf surfaces.",
            "Keep soil evenly moist to prevent blossom end rot."
        ],
        "treatment": [
            "No disease treatment required.",
            "Maintain balanced fertilization with calcium and magnesium supplements."
        ],
        "prevention": [
            "Stake or cage plants off the ground.",
            "Apply mulch layer around base.",
            "Prune lowest branches 30 cm above ground once plants are established to prevent soil splash."
        ],
        "precautions": "Avoid irregular watering which triggers physiological blossom end rot and fruit cracking."
    }
}


def get_disease_info(raw_class_name: str) -> Dict[str, Any]:
    """
    Retrieve structured agronomic information for any of the 38 PlantVillage classes.
    Falls back gracefully if an unknown class name is passed.
    """
    if raw_class_name in DISEASE_DATABASE:
        return DISEASE_DATABASE[raw_class_name]

    # Try fuzzy matching
    for key, data in DISEASE_DATABASE.items():
        if key.lower() == raw_class_name.lower():
            return data
        # Check condition substring
        if "___" in key and "___" in raw_class_name:
            c1, d1 = key.split("___", 1)
            c2, d2 = raw_class_name.split("___", 1)
            if c1.lower() == c2.lower() and d1.lower() == d2.lower():
                return data

    # Default fallback
    crop = raw_class_name.split("___")[0].replace("_", " ").strip() if "___" in raw_class_name else "Crop"
    cond = raw_class_name.split("___")[1].replace("_", " ").strip() if "___" in raw_class_name else raw_class_name
    is_healthy = "healthy" in raw_class_name.lower()

    return {
        "crop": crop,
        "condition": cond if not is_healthy else "Healthy Foliage",
        "scientific_name": "Plant species",
        "pathogen_type": "Unknown" if not is_healthy else "None",
        "is_healthy": is_healthy,
        "severity_baseline": "None" if is_healthy else "Moderate",
        "symptoms": ["Inspect foliage for discoloration or lesions."] if not is_healthy else ["Healthy foliage observed."],
        "favoring_conditions": "Varies by local microclimate and weather.",
        "immediate_actions": [
            "Isolate affected foliage." if not is_healthy else "Continue routine plant care.",
            "Consult local agricultural extension for localized management guidelines."
        ],
        "treatment": [
            "Apply targeted treatment based on professional laboratory diagnosis." if not is_healthy else "No treatment required."
        ],
        "prevention": [
            "Ensure adequate spacing and drip irrigation.",
            "Rotate crops on a 2-3 year cycle."
        ],
        "precautions": "Always follow pesticide product label requirements and local environmental regulations."
    }
