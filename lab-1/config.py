BASE = "https://cvetovik.com"
OUT  = "data/cvetovik2.csv"

COLS = ["product_id","name","rating","rating_count","num_flowers",
    "aroma","composition_flowers","target_price","bonus","city"]

UA = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/123 Safari/537.36",]

FLOWERS = {"роза":"роза","розы":"роза","роз":"роза",
    "хризантема":"хризантема","хризантемы":"хризантема","хризантем":"хризантема",
    "сантини":"хризантема","кустовая":"хризантема","бакарди":"хризантема",

    "гвоздика":"гвоздика","гвоздики":"гвоздика","диантус":"гвоздика",

    "гербера":"гербера","герберы":"гербера",

    "лилия":"лилия","лилии":"лилия",

    "гортензия":"гортензия","гортензии":"гортензия",

    "матиола":"матиола","маттиола":"матиола",

    "альстромерия":"альстромерия","альстромерии":"альстромерия",

    "гиацинт":"гиацинт","гиацинты":"гиацинт",

    "ирис":"ирис","ирисы":"ирис",

    "эустома":"эустома","эустомы":"эустома","лизиантус":"эустома",

    "ромашка":"ромашка","ромашки":"ромашка",

    "подсолнух":"подсолнух","подсолнухи":"подсолнух",

    "гладиолус":"гладиолус","гладиолусы":"гладиолус",

    "фрезия":"фрезия","фрезии":"фрезия",

    "сухоцветы":"сухоцветы","сухоцвет":"сухоцветы",

    "гипсофила":"гипсофила",

    "нарцисс":"нарцисс","нарциссы":"нарцисс",

    "тюльпан":"тюльпан","тюльпаны":"тюльпан",

    "пион":"пион","пионы":"пион",

    "ранункулюс":"ранункулюс","ранункулюсы":"ранункулюс",

    "левкой":"левкой","левкои":"левкой",

    "орхидея":"орхидея","орхидеи":"орхидея",

    "эвкалипт":"эвкалипт"}

NON_FLOWER_TOKENS = {
    "упаковка","лента","пленка","бумага","оазис","корзина","фисташка","зелень","злак"
}
CATEGORIES = [
    ("https://moscow.cvetovik.com/catalog/zakritaya_rasprodazha/", 1),
    ("https://moscow.cvetovik.com/catalog/rozi_1/buketi_iz_roz/", 5),
    ("https://moscow.cvetovik.com/catalog/tsveti/xrizantemi/", 2),
    ("https://moscow.cvetovik.com/catalog/tsveti/gvozdiki/", 2),
    ("https://moscow.cvetovik.com/catalog/tsveti/gerberi/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/lilii/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/gortenziya/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/mattiola/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/alstromeriya/", 2),
    ("https://moscow.cvetovik.com/catalog/tsveti/giatsinti/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/irisi/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/eustoma_liziantus/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/romashki/", 2),
    ("https://moscow.cvetovik.com/catalog/tsveti/podsolnuhi/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/gladiolusi/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/frezii/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/suhotsveti/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/gipsofila/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/nartsissi/", 1),
    ("https://moscow.cvetovik.com/catalog/tsveti/tyulpani/", 2),
    ("https://moscow.cvetovik.com/catalog/tsveti/pioni/", 1),
    ("https://cvetovik.com/catalog/tsveti/xrizantemi/", 2),
    ("https://cvetovik.com/catalog/tsveti/gvozdiki/", 2),
    ("https://cvetovik.com/catalog/tsveti/gerberi/", 1),
    ("https://cvetovik.com/catalog/tsveti/lilii/", 1),
    ("https://cvetovik.com/catalog/tsveti/gortenziya/", 1),
    ("https://cvetovik.com/catalog/tsveti/mattiola/", 1),
    ("https://cvetovik.com/catalog/tsveti/alstromeriya/", 2),
    ("https://cvetovik.com/catalog/tsveti/giatsinti/", 1),
    ("https://cvetovik.com/catalog/tsveti/irisi/", 1),
    ("https://cvetovik.com/catalog/tsveti/eustoma_liziantus/", 1),
    ("https://cvetovik.com/catalog/tsveti/romashki/", 1),
    ("https://cvetovik.com/catalog/tsveti/podsolnuhi/", 1),
    ("https://cvetovik.com/catalog/tsveti/gladiolusi/", 1),
    ("https://cvetovik.com/catalog/tsveti/frezii/", 1),
    ("https://cvetovik.com/catalog/tsveti/suhotsveti/", 1),
    ("https://cvetovik.com/catalog/tsveti/gipsofila/", 1),
    ("https://cvetovik.com/catalog/tsveti/nartsissi/", 1),
    ("https://cvetovik.com/catalog/tsveti/tyulpani/", 2),
    ("https://cvetovik.com/catalog/tsveti/pioni/", 1),
    ("https://pskov.cvetovik.com/catalog/tsveti/xrizantemi/", 2),
("https://pskov.cvetovik.com/catalog/tsveti/gvozdiki/", 2),
("https://pskov.cvetovik.com/catalog/tsveti/gerberi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/lilii/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/gortenziya/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/levkoi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/alstromeriya/", 2),
("https://pskov.cvetovik.com/catalog/tsveti/giatsinti/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/irisi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/eustoma_liziantus/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/romashki/", 2),
("https://pskov.cvetovik.com/catalog/tsveti/podsolnuhi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/gladiolusi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/frezii/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/gipsofila/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/nartsissi/", 1),
("https://pskov.cvetovik.com/catalog/tsveti/tyulpani/", 2),
("https://pskov.cvetovik.com/catalog/tsveti/pioni/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/xrizantemi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/gvozdiki/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/gerberi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/lilii/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/gortenziya/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/levkoi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/alstromeriya/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/giatsinti/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/irisi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/eustoma_liziantus/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/romashki/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/podsolnuhi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/gipsofila/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/nartsissi/", 1),
("https://krasnodar.cvetovik.com/catalog/tsveti/tyulpani/", 2),
("https://kazan.cvetovik.com/catalog/tsveti/tyulpani/", 2),
("https://kazan.cvetovik.com/catalog/tsveti/gipsofila/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/suhotsveti/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/frezii/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/podsolnuhi/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/romashki/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/eustoma_liziantus/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/irisi/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/alstromeriya/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/levkoi/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/gortenziya/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/lilii/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/gerberi/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/gvozdiki/", 1),
("https://kazan.cvetovik.com/catalog/tsveti/xrizantemi/", 1)]
