"""UI strings for the 5 site languages (en, ar, fr, es, de)."""

LANGS = ["en", "ar", "fr", "es", "de"]
LANG_NAMES = {"en": "English", "ar": "العربية", "fr": "Français", "es": "Español", "de": "Deutsch"}
RTL = {"ar"}

T = {
"en": dict(
    trending="Trending now", trending_sub="New and fast-rising open-source repos, found by our bot on GitHub and updated every day.", stars_day="stars / day", gained="+{n} in 24h", new_badge="NEW", updated_on="Updated", see_trending="See all trending",
    tagline="The 1,000 open-source projects that matter — and the Claude skills inside them",
    hero_sub="Ranked by real growth, activity and future potential. Every skill, agent and command is a plain file you can read before you install it.",
    search="Search repos, skills, agents…", repos="Repositories", skills="Skills", agents="Agents", commands="Commands",
    categories="Categories", top="Top-ranked repos", all_in="All repos in", rank="Rank", stars="Stars", forks="Forks",
    lang="Language", license="License", created="Created", updated="Last update", score="Future score", tier="Tier",
    why="Why it has potential", get="Get it", clone_hint="Clone a lightweight copy (latest commit only):",
    related="Related repos", from_repo="Skills & agents from this repo", view_github="View on GitHub",
    install="Install", install_hint="Copy this folder into your Claude Code project (needs Node.js):",
    install_user="Or install it for every project:", source="Source", content="File content",
    home="Home", about="About", privacy="Privacy", terms="Terms", contact="Contact", guides="Guides",
    theme="Toggle theme", components="components", projects="projects", open_source="Open source on GitHub",
    browse_all="Browse all", items="items", filter="Filter…", attribution="Made by its original authors and shared under",
    attribution2="We show it unchanged, with credit and a link to the source.",
    days_ago="{n} days ago", today="today", not_found="Page not found", back_home="Back to home",
    star_year="stars / year", size="Size",
    summary=("{name} is {a_type} written in {lang}, first published on {created}. It has {stars} stars and {forks} forks, "
             "and gains about {spy} new stars a year. Its code was last updated {upd}. "
             "It is released under the {lic} license: {lic_note}"),
    summary2="OpenShelf gives it a future score of {score}/100 (tier {tier}) because it shows: {reasons}.",
    lic_permissive="you can use, change and sell it, as long as you keep the copyright notice.",
    lic_copyleft="you can use it freely, but if you distribute (or for AGPL, host) a changed version you must share your source code too.",
    lic_other="check the repository's license file before using it in a product.",
    reasons={"actively updated": "active updates", "hot AI trend": "a hot AI trend", "very fast growth": "very fast growth",
             "fast growth": "fast growth", "huge community": "a huge community", "your pick": "an editor's pick",
             "slow updates – check": "slow updates (check before relying on it)"},
    types={"Skill / MCP": "a Claude skill / MCP project", "App / Tool": "an app or tool", "Agent": "an AI agent",
           "Model / ML": "a model / machine-learning project", "Library / Framework": "a library or framework"},
    about_body=("<p>OpenShelf is an independent directory of the 1,000 open-source repositories we think will matter most "
                "over the next years: AI agents, Claude Code skills and MCP servers, LLM apps, self-hosted software, developer tools and more.</p>"
                "<p><b>How repos are ranked.</b> We pulled more than 5,000 candidate repositories from the public GitHub API and scored each one "
                "on stars gained per year, total community size, how recently it was updated and whether it is part of a fast-moving trend. "
                "The result is a future score from 0 to 100 and a tier from S to C.</p>"
                "<p><b>Where skills and agents come from.</b> Every skill, agent and command on this site was written by the authors of an open-source "
                "repository with a permissive license (MIT, Apache-2.0, BSD, ISC, MPL, CC0 or Unlicense). We show each file unchanged, with its author, "
                "license and a link to the original. If you are an author and want a file removed or corrected, open an issue on our GitHub repository.</p>"
                "<p>OpenShelf is not affiliated with GitHub or Anthropic.</p>"),
    privacy_body=("<p>This site is static: it has no accounts and stores nothing about you on our servers. Your theme and language choice are kept in your browser's local storage.</p>"
                  "<p>We may use privacy-friendly analytics and, in the future, Google AdSense. Google uses cookies to show ads; you can manage ad personalisation at "
                  "<a href='https://adssettings.google.com'>adssettings.google.com</a>. Where the law requires it, we ask for your consent first.</p>"
                  "<p>Questions: open an issue on our GitHub repository.</p>"),
    terms_body=("<p>Content on OpenShelf is provided as is, for information. Each listed project and file belongs to its authors and is governed by its own license. "
                "Read any skill, hook or agent before you install it: they can run code on your machine.</p>"),
),
"ar": dict(
    trending="الأكثر رواجًا الآن", trending_sub="مستودعات مفتوحة المصدر جديدة وسريعة الصعود، يكتشفها روبوتنا على GitHub ويحدّثها يوميًا.", stars_day="نجمة / يوم", gained="+{n} خلال 24 ساعة", new_badge="جديد", updated_on="آخر تحديث", see_trending="كل المستودعات الرائجة",
    tagline="أهم 1000 مشروع مفتوح المصدر — ومهارات Claude الموجودة داخلها",
    hero_sub="مرتبة حسب النمو الحقيقي والنشاط وإمكانات المستقبل. كل مهارة ووكيل وأمر هو ملف نصي يمكنك قراءته قبل تثبيته.",
    search="ابحث في المستودعات والمهارات والوكلاء…", repos="المستودعات", skills="المهارات", agents="الوكلاء", commands="الأوامر",
    categories="الفئات", top="أعلى المستودعات ترتيبًا", all_in="كل المستودعات في", rank="الترتيب", stars="النجوم", forks="النسخ",
    lang="اللغة", license="الترخيص", created="تاريخ الإنشاء", updated="آخر تحديث", score="درجة المستقبل", tier="المستوى",
    why="لماذا لديه إمكانات", get="احصل عليه", clone_hint="انسخ نسخة خفيفة (آخر إصدار فقط):",
    related="مستودعات مشابهة", from_repo="مهارات ووكلاء من هذا المستودع", view_github="عرض على GitHub",
    install="التثبيت", install_hint="انسخ هذا المجلد إلى مشروع Claude Code (يتطلب Node.js):",
    install_user="أو ثبّته لكل المشاريع:", source="المصدر", content="محتوى الملف",
    home="الرئيسية", about="من نحن", privacy="الخصوصية", terms="الشروط", contact="اتصل بنا", guides="أدلة",
    theme="تبديل المظهر", components="عنصر", projects="مشروع", open_source="مفتوح المصدر على GitHub",
    browse_all="تصفح الكل", items="عنصر", filter="تصفية…", attribution="من إنشاء مؤلفيه الأصليين ومنشور بترخيص",
    attribution2="نعرضه دون تغيير، مع ذكر المصدر ورابط إليه.",
    days_ago="قبل {n} يوم", today="اليوم", not_found="الصفحة غير موجودة", back_home="العودة للرئيسية",
    star_year="نجمة / سنة", size="الحجم",
    summary=("{name} هو {a_type} مكتوب بلغة {lang}، نُشر لأول مرة في {created}. لديه {stars} نجمة و{forks} نسخة، "
             "ويكسب نحو {spy} نجمة جديدة سنويًا. آخر تحديث لكوده كان {upd}. "
             "صدر بترخيص {lic}: {lic_note}"),
    summary2="يمنحه OpenShelf درجة مستقبل {score}/100 (المستوى {tier}) لأنه يُظهر: {reasons}.",
    lic_permissive="يمكنك استخدامه وتعديله وبيعه، بشرط الإبقاء على إشعار حقوق النشر.",
    lic_copyleft="يمكنك استخدامه بحرية، لكن إذا وزّعت (أو استضفت في حالة AGPL) نسخة معدلة فيجب أن تشارك الكود المصدري أيضًا.",
    lic_other="راجع ملف الترخيص في المستودع قبل استخدامه في منتج.",
    reasons={"actively updated": "تحديثات نشطة", "hot AI trend": "توجه رائج في الذكاء الاصطناعي", "very fast growth": "نمو سريع جدًا",
             "fast growth": "نمو سريع", "huge community": "مجتمع ضخم", "your pick": "اختيار المحرر",
             "slow updates – check": "تحديثات بطيئة (تحقق قبل الاعتماد عليه)"},
    types={"Skill / MCP": "مشروع مهارات Claude / MCP", "App / Tool": "تطبيق أو أداة", "Agent": "وكيل ذكاء اصطناعي",
           "Model / ML": "مشروع نموذج / تعلم آلي", "Library / Framework": "مكتبة أو إطار عمل"},
    about_body=("<p>OpenShelf دليل مستقل لأهم 1000 مستودع مفتوح المصدر نتوقع أن تكون الأهم في السنوات القادمة: وكلاء الذكاء الاصطناعي، "
                "مهارات Claude Code وخوادم MCP، تطبيقات النماذج اللغوية، البرمجيات المستضافة ذاتيًا، أدوات المطورين وغيرها.</p>"
                "<p><b>كيف نرتب المستودعات.</b> جمعنا أكثر من 5000 مستودع مرشح من واجهة GitHub العامة وقيّمنا كلًا منها حسب النجوم المكتسبة سنويًا، "
                "وحجم المجتمع، وحداثة التحديث، وارتباطه بتوجه سريع النمو. النتيجة درجة مستقبل من 0 إلى 100 ومستوى من S إلى C.</p>"
                "<p><b>مصدر المهارات والوكلاء.</b> كل مهارة ووكيل وأمر في الموقع كتبه مؤلفو مستودع مفتوح المصدر بترخيص متساهل "
                "(MIT أو Apache-2.0 أو BSD أو ISC أو MPL أو CC0 أو Unlicense). نعرض كل ملف دون تغيير مع اسم المؤلف والترخيص ورابط الأصل. "
                "إذا كنت مؤلفًا وتريد حذف ملف أو تصحيحه، افتح طلبًا (issue) في مستودعنا على GitHub.</p>"
                "<p>OpenShelf غير تابع لـ GitHub أو Anthropic.</p>"),
    privacy_body=("<p>هذا الموقع ثابت: لا توجد حسابات ولا نخزن أي معلومات عنك على خوادمنا. يُحفظ اختيارك للمظهر واللغة في متصفحك فقط.</p>"
                  "<p>قد نستخدم إحصاءات تحترم الخصوصية، وفي المستقبل Google AdSense. تستخدم Google ملفات تعريف الارتباط لعرض الإعلانات، ويمكنك إدارة تخصيص الإعلانات من "
                  "<a href='https://adssettings.google.com'>adssettings.google.com</a>. حيث يفرض القانون ذلك، نطلب موافقتك أولًا.</p>"
                  "<p>للأسئلة: افتح طلبًا في مستودعنا على GitHub.</p>"),
    terms_body=("<p>يُقدَّم محتوى OpenShelf كما هو، لأغراض المعلومات. كل مشروع وملف مدرج ملك لمؤلفيه ويخضع لترخيصه الخاص. "
                "اقرأ أي مهارة أو hook أو وكيل قبل تثبيته: فقد تشغّل كودًا على جهازك.</p>"),
),
"fr": dict(
    trending="Tendances", trending_sub="Nouveaux dépôts open source en pleine ascension, repérés par notre bot sur GitHub et mis à jour chaque jour.", stars_day="étoiles / jour", gained="+{n} en 24 h", new_badge="NOUVEAU", updated_on="Mis à jour", see_trending="Toutes les tendances",
    tagline="Les 1 000 projets open source qui comptent — et les skills Claude qu'ils contiennent",
    hero_sub="Classés selon leur croissance réelle, leur activité et leur potentiel. Chaque skill, agent et commande est un simple fichier que vous pouvez lire avant de l'installer.",
    search="Rechercher dépôts, skills, agents…", repos="Dépôts", skills="Skills", agents="Agents", commands="Commandes",
    categories="Catégories", top="Dépôts les mieux classés", all_in="Tous les dépôts :", rank="Rang", stars="Étoiles", forks="Forks",
    lang="Langage", license="Licence", created="Créé le", updated="Dernière mise à jour", score="Score d'avenir", tier="Niveau",
    why="Pourquoi il a du potentiel", get="Le récupérer", clone_hint="Cloner une copie légère (dernier commit seulement) :",
    related="Dépôts similaires", from_repo="Skills et agents de ce dépôt", view_github="Voir sur GitHub",
    install="Installer", install_hint="Copiez ce dossier dans votre projet Claude Code (Node.js requis) :",
    install_user="Ou installez-le pour tous vos projets :", source="Source", content="Contenu du fichier",
    home="Accueil", about="À propos", privacy="Confidentialité", terms="Conditions", contact="Contact", guides="Guides",
    theme="Changer de thème", components="composants", projects="projets", open_source="Open source sur GitHub",
    browse_all="Tout parcourir", items="éléments", filter="Filtrer…", attribution="Créé par ses auteurs d'origine et partagé sous licence",
    attribution2="Nous l'affichons sans modification, avec crédit et lien vers la source.",
    days_ago="il y a {n} jours", today="aujourd'hui", not_found="Page introuvable", back_home="Retour à l'accueil",
    star_year="étoiles / an", size="Taille",
    summary=("{name} est {a_type} écrit en {lang}, publié pour la première fois le {created}. Il compte {stars} étoiles et {forks} forks, "
             "et gagne environ {spy} nouvelles étoiles par an. Son code a été mis à jour {upd}. "
             "Il est publié sous licence {lic} : {lic_note}"),
    summary2="OpenShelf lui attribue un score d'avenir de {score}/100 (niveau {tier}) car il présente : {reasons}.",
    lic_permissive="vous pouvez l'utiliser, le modifier et le vendre, à condition de conserver la mention de copyright.",
    lic_copyleft="vous pouvez l'utiliser librement, mais si vous distribuez (ou, pour l'AGPL, hébergez) une version modifiée, vous devez aussi partager votre code source.",
    lic_other="consultez le fichier de licence du dépôt avant de l'utiliser dans un produit.",
    reasons={"actively updated": "des mises à jour actives", "hot AI trend": "une tendance IA forte", "very fast growth": "une croissance très rapide",
             "fast growth": "une croissance rapide", "huge community": "une énorme communauté", "your pick": "un choix de la rédaction",
             "slow updates – check": "des mises à jour lentes (à vérifier)"},
    types={"Skill / MCP": "un projet de skills Claude / MCP", "App / Tool": "une application ou un outil", "Agent": "un agent IA",
           "Model / ML": "un projet de modèle / machine learning", "Library / Framework": "une bibliothèque ou un framework"},
    about_body=("<p>OpenShelf est un annuaire indépendant des 1 000 dépôts open source qui, selon nous, compteront le plus dans les prochaines années : "
                "agents IA, skills Claude Code et serveurs MCP, applications LLM, logiciels auto-hébergés, outils pour développeurs, etc.</p>"
                "<p><b>Comment les dépôts sont classés.</b> Nous avons extrait plus de 5 000 dépôts candidats de l'API publique de GitHub et noté chacun "
                "selon les étoiles gagnées par an, la taille de sa communauté, la fraîcheur de ses mises à jour et son appartenance à une tendance rapide. "
                "Résultat : un score d'avenir de 0 à 100 et un niveau de S à C.</p>"
                "<p><b>D'où viennent les skills et agents.</b> Chaque skill, agent et commande a été écrit par les auteurs d'un dépôt open source sous licence permissive "
                "(MIT, Apache-2.0, BSD, ISC, MPL, CC0 ou Unlicense). Nous affichons chaque fichier sans modification, avec son auteur, sa licence et un lien vers l'original. "
                "Si vous êtes l'auteur et souhaitez qu'un fichier soit retiré ou corrigé, ouvrez une issue sur notre dépôt GitHub.</p>"
                "<p>OpenShelf n'est affilié ni à GitHub ni à Anthropic.</p>"),
    privacy_body=("<p>Ce site est statique : pas de comptes, et nous ne stockons rien sur vous sur nos serveurs. Vos choix de thème et de langue restent dans le stockage local de votre navigateur.</p>"
                  "<p>Nous pouvons utiliser des statistiques respectueuses de la vie privée et, plus tard, Google AdSense. Google utilise des cookies pour afficher des annonces ; gérez la personnalisation sur "
                  "<a href='https://adssettings.google.com'>adssettings.google.com</a>. Lorsque la loi l'exige, nous demandons d'abord votre consentement.</p>"
                  "<p>Questions : ouvrez une issue sur notre dépôt GitHub.</p>"),
    terms_body=("<p>Le contenu de OpenShelf est fourni tel quel, à titre informatif. Chaque projet et fichier appartient à ses auteurs et relève de sa propre licence. "
                "Lisez chaque skill, hook ou agent avant de l'installer : ils peuvent exécuter du code sur votre machine.</p>"),
),
"es": dict(
    trending="Tendencias", trending_sub="Repos open source nuevos y en rápido ascenso, detectados por nuestro bot en GitHub y actualizados cada día.", stars_day="estrellas / día", gained="+{n} en 24 h", new_badge="NUEVO", updated_on="Actualizado", see_trending="Ver todas las tendencias",
    tagline="Los 1.000 proyectos open source que importan — y las skills de Claude que contienen",
    hero_sub="Ordenados por crecimiento real, actividad y potencial de futuro. Cada skill, agente y comando es un archivo que puedes leer antes de instalarlo.",
    search="Buscar repos, skills, agentes…", repos="Repositorios", skills="Skills", agents="Agentes", commands="Comandos",
    categories="Categorías", top="Repos mejor clasificados", all_in="Todos los repos de", rank="Puesto", stars="Estrellas", forks="Forks",
    lang="Lenguaje", license="Licencia", created="Creado", updated="Última actualización", score="Puntuación de futuro", tier="Nivel",
    why="Por qué tiene potencial", get="Obtenerlo", clone_hint="Clona una copia ligera (solo el último commit):",
    related="Repos relacionados", from_repo="Skills y agentes de este repo", view_github="Ver en GitHub",
    install="Instalar", install_hint="Copia esta carpeta en tu proyecto de Claude Code (requiere Node.js):",
    install_user="O instálalo para todos tus proyectos:", source="Fuente", content="Contenido del archivo",
    home="Inicio", about="Acerca de", privacy="Privacidad", terms="Términos", contact="Contacto", guides="Guías",
    theme="Cambiar tema", components="componentes", projects="proyectos", open_source="Código abierto en GitHub",
    browse_all="Ver todo", items="elementos", filter="Filtrar…", attribution="Creado por sus autores originales y compartido bajo la licencia",
    attribution2="Lo mostramos sin cambios, con crédito y enlace a la fuente.",
    days_ago="hace {n} días", today="hoy", not_found="Página no encontrada", back_home="Volver al inicio",
    star_year="estrellas / año", size="Tamaño",
    summary=("{name} es {a_type} escrito en {lang}, publicado por primera vez el {created}. Tiene {stars} estrellas y {forks} forks, "
             "y gana unas {spy} estrellas nuevas al año. Su código se actualizó {upd}. "
             "Se publica bajo la licencia {lic}: {lic_note}"),
    summary2="OpenShelf le da una puntuación de futuro de {score}/100 (nivel {tier}) porque muestra: {reasons}.",
    lic_permissive="puedes usarlo, modificarlo y venderlo, siempre que conserves el aviso de copyright.",
    lic_copyleft="puedes usarlo libremente, pero si distribuyes (o, con AGPL, alojas) una versión modificada debes compartir también tu código fuente.",
    lic_other="revisa el archivo de licencia del repositorio antes de usarlo en un producto.",
    reasons={"actively updated": "actualizaciones activas", "hot AI trend": "una tendencia de IA en auge", "very fast growth": "crecimiento muy rápido",
             "fast growth": "crecimiento rápido", "huge community": "una comunidad enorme", "your pick": "una elección del editor",
             "slow updates – check": "actualizaciones lentas (compruébalo antes)"},
    types={"Skill / MCP": "un proyecto de skills de Claude / MCP", "App / Tool": "una app o herramienta", "Agent": "un agente de IA",
           "Model / ML": "un proyecto de modelo / machine learning", "Library / Framework": "una biblioteca o framework"},
    about_body=("<p>OpenShelf es un directorio independiente de los 1.000 repositorios open source que creemos que más importarán en los próximos años: "
                "agentes de IA, skills de Claude Code y servidores MCP, apps de LLM, software autoalojado, herramientas para desarrolladores y más.</p>"
                "<p><b>Cómo se clasifican.</b> Obtuvimos más de 5.000 repositorios candidatos de la API pública de GitHub y puntuamos cada uno "
                "según las estrellas ganadas por año, el tamaño de su comunidad, lo reciente de sus actualizaciones y si forma parte de una tendencia rápida. "
                "El resultado es una puntuación de futuro de 0 a 100 y un nivel de S a C.</p>"
                "<p><b>De dónde vienen las skills y agentes.</b> Cada skill, agente y comando lo escribieron los autores de un repositorio open source con licencia permisiva "
                "(MIT, Apache-2.0, BSD, ISC, MPL, CC0 o Unlicense). Mostramos cada archivo sin cambios, con su autor, licencia y enlace al original. "
                "Si eres autor y quieres que retiremos o corrijamos un archivo, abre un issue en nuestro repositorio de GitHub.</p>"
                "<p>OpenShelf no está afiliado a GitHub ni a Anthropic.</p>"),
    privacy_body=("<p>Este sitio es estático: no hay cuentas y no guardamos nada sobre ti en nuestros servidores. Tu tema e idioma se guardan en el almacenamiento local de tu navegador.</p>"
                  "<p>Podemos usar analíticas respetuosas con la privacidad y, más adelante, Google AdSense. Google usa cookies para mostrar anuncios; gestiona la personalización en "
                  "<a href='https://adssettings.google.com'>adssettings.google.com</a>. Cuando la ley lo exige, pedimos tu consentimiento primero.</p>"
                  "<p>Preguntas: abre un issue en nuestro repositorio de GitHub.</p>"),
    terms_body=("<p>El contenido de OpenShelf se ofrece tal cual, con fines informativos. Cada proyecto y archivo pertenece a sus autores y se rige por su propia licencia. "
                "Lee cualquier skill, hook o agente antes de instalarlo: pueden ejecutar código en tu equipo.</p>"),
),
"de": dict(
    trending="Gerade im Trend", trending_sub="Neue, schnell wachsende Open-Source-Repos, täglich von unserem Bot auf GitHub gefunden und aktualisiert.", stars_day="Sterne / Tag", gained="+{n} in 24 Std.", new_badge="NEU", updated_on="Aktualisiert", see_trending="Alle Trends ansehen",
    tagline="Die 1.000 Open-Source-Projekte, die zählen — und die Claude-Skills darin",
    hero_sub="Gerankt nach echtem Wachstum, Aktivität und Zukunftspotenzial. Jeder Skill, Agent und Befehl ist eine einfache Datei, die du vor der Installation lesen kannst.",
    search="Repos, Skills, Agents suchen…", repos="Repositories", skills="Skills", agents="Agents", commands="Befehle",
    categories="Kategorien", top="Bestplatzierte Repos", all_in="Alle Repos in", rank="Rang", stars="Sterne", forks="Forks",
    lang="Sprache", license="Lizenz", created="Erstellt", updated="Letztes Update", score="Zukunftswert", tier="Stufe",
    why="Warum es Potenzial hat", get="Herunterladen", clone_hint="Leichte Kopie klonen (nur der letzte Commit):",
    related="Ähnliche Repos", from_repo="Skills & Agents aus diesem Repo", view_github="Auf GitHub ansehen",
    install="Installieren", install_hint="Kopiere diesen Ordner in dein Claude-Code-Projekt (Node.js nötig):",
    install_user="Oder für alle Projekte installieren:", source="Quelle", content="Dateiinhalt",
    home="Start", about="Über uns", privacy="Datenschutz", terms="Bedingungen", contact="Kontakt", guides="Ratgeber",
    theme="Design wechseln", components="Komponenten", projects="Projekte", open_source="Open Source auf GitHub",
    browse_all="Alle ansehen", items="Einträge", filter="Filtern…", attribution="Erstellt von den ursprünglichen Autoren und geteilt unter der Lizenz",
    attribution2="Wir zeigen es unverändert, mit Nennung und Link zur Quelle.",
    days_ago="vor {n} Tagen", today="heute", not_found="Seite nicht gefunden", back_home="Zur Startseite",
    star_year="Sterne / Jahr", size="Größe",
    summary=("{name} ist {a_type}, geschrieben in {lang} und erstmals am {created} veröffentlicht. Es hat {stars} Sterne und {forks} Forks "
             "und gewinnt etwa {spy} neue Sterne pro Jahr. Der Code wurde {upd} zuletzt aktualisiert. "
             "Es steht unter der Lizenz {lic}: {lic_note}"),
    summary2="OpenShelf gibt ihm einen Zukunftswert von {score}/100 (Stufe {tier}), weil es Folgendes zeigt: {reasons}.",
    lic_permissive="du darfst es nutzen, ändern und verkaufen, solange der Copyright-Hinweis erhalten bleibt.",
    lic_copyleft="du darfst es frei nutzen, aber wenn du eine geänderte Version verbreitest (bei AGPL auch hostest), musst du deinen Quellcode ebenfalls teilen.",
    lic_other="prüfe die Lizenzdatei des Repos, bevor du es in einem Produkt einsetzt.",
    reasons={"actively updated": "aktive Updates", "hot AI trend": "einen heißen KI-Trend", "very fast growth": "sehr schnelles Wachstum",
             "fast growth": "schnelles Wachstum", "huge community": "eine riesige Community", "your pick": "eine Empfehlung der Redaktion",
             "slow updates – check": "langsame Updates (vorher prüfen)"},
    types={"Skill / MCP": "ein Claude-Skill-/MCP-Projekt", "App / Tool": "eine App bzw. ein Tool", "Agent": "ein KI-Agent",
           "Model / ML": "ein Modell-/Machine-Learning-Projekt", "Library / Framework": "eine Bibliothek bzw. ein Framework"},
    about_body=("<p>OpenShelf ist ein unabhängiges Verzeichnis der 1.000 Open-Source-Repositories, die unserer Meinung nach in den nächsten Jahren am wichtigsten werden: "
                "KI-Agents, Claude-Code-Skills und MCP-Server, LLM-Apps, selbst gehostete Software, Entwickler-Tools und mehr.</p>"
                "<p><b>Wie gerankt wird.</b> Wir haben über 5.000 Kandidaten über die öffentliche GitHub-API abgerufen und jedes Repo nach Sternen pro Jahr, "
                "Community-Größe, Aktualität der Updates und Zugehörigkeit zu einem schnell wachsenden Trend bewertet. "
                "Ergebnis: ein Zukunftswert von 0 bis 100 und eine Stufe von S bis C.</p>"
                "<p><b>Woher Skills und Agents stammen.</b> Jeder Skill, Agent und Befehl wurde von den Autoren eines Open-Source-Repos mit freizügiger Lizenz "
                "(MIT, Apache-2.0, BSD, ISC, MPL, CC0 oder Unlicense) geschrieben. Wir zeigen jede Datei unverändert, mit Autor, Lizenz und Link zum Original. "
                "Wenn du Autor bist und eine Datei entfernen oder korrigieren lassen willst, eröffne ein Issue in unserem GitHub-Repository.</p>"
                "<p>OpenShelf ist weder mit GitHub noch mit Anthropic verbunden.</p>"),
    privacy_body=("<p>Diese Seite ist statisch: keine Konten, und wir speichern nichts über dich auf unseren Servern. Design- und Sprachwahl bleiben im lokalen Speicher deines Browsers.</p>"
                  "<p>Wir nutzen ggf. datenschutzfreundliche Statistiken und künftig Google AdSense. Google verwendet Cookies für Anzeigen; die Personalisierung verwaltest du unter "
                  "<a href='https://adssettings.google.com'>adssettings.google.com</a>. Wo gesetzlich nötig, fragen wir vorher nach deiner Einwilligung.</p>"
                  "<p>Fragen: eröffne ein Issue in unserem GitHub-Repository.</p>"),
    terms_body=("<p>Die Inhalte von OpenShelf werden ohne Gewähr zur Information bereitgestellt. Jedes Projekt und jede Datei gehört den jeweiligen Autoren und unterliegt der eigenen Lizenz. "
                "Lies jeden Skill, Hook oder Agent vor der Installation: Sie können Code auf deinem Rechner ausführen.</p>"),
),
}

CATS = {
 "AI Agents": dict(en="AI Agents", ar="وكلاء الذكاء الاصطناعي", fr="Agents IA", es="Agentes de IA", de="KI-Agents"),
 "LLM & GenAI": dict(en="LLM & GenAI", ar="النماذج اللغوية والذكاء التوليدي", fr="LLM et IA générative", es="LLM e IA generativa", de="LLM & GenAI"),
 "General / Other": dict(en="General & Other", ar="عام ومتنوع", fr="Général et divers", es="General y otros", de="Allgemein & Sonstiges"),
 "Skills & MCP": dict(en="Claude Skills & MCP", ar="مهارات Claude و MCP", fr="Skills Claude et MCP", es="Skills de Claude y MCP", de="Claude-Skills & MCP"),
 "Developer Tools": dict(en="Developer Tools", ar="أدوات المطورين", fr="Outils pour développeurs", es="Herramientas para desarrolladores", de="Entwickler-Tools"),
 "Automation": dict(en="Automation", ar="الأتمتة", fr="Automatisation", es="Automatización", de="Automatisierung"),
 "Machine Learning": dict(en="Machine Learning", ar="تعلم الآلة", fr="Machine learning", es="Aprendizaje automático", de="Maschinelles Lernen"),
 "Self-Hosted Apps": dict(en="Self-Hosted Apps", ar="تطبيقات مستضافة ذاتيًا", fr="Applis auto-hébergées", es="Apps autoalojadas", de="Selbst gehostete Apps"),
 "Web & Frameworks": dict(en="Web & Frameworks", ar="الويب وأطر العمل", fr="Web et frameworks", es="Web y frameworks", de="Web & Frameworks"),
 "Data & Databases": dict(en="Data & Databases", ar="البيانات وقواعدها", fr="Données et bases de données", es="Datos y bases de datos", de="Daten & Datenbanken"),
 "Image/Video/Audio AI": dict(en="Image, Video & Audio AI", ar="ذكاء الصور والفيديو والصوت", fr="IA image, vidéo et audio", es="IA de imagen, vídeo y audio", de="Bild-, Video- & Audio-KI"),
 "Security": dict(en="Security", ar="الأمن", fr="Sécurité", es="Seguridad", de="Sicherheit"),
 "Your Picks": dict(en="Editor's Picks", ar="اختيارات المحرر", fr="Choix de la rédaction", es="Selección del editor", de="Redaktionstipps"),
 "Productivity Apps": dict(en="Productivity Apps", ar="تطبيقات الإنتاجية", fr="Applis de productivité", es="Apps de productividad", de="Produktivitäts-Apps"),
 "Trading & Finance": dict(en="Trading & Finance", ar="التداول والمال", fr="Trading et finance", es="Trading y finanzas", de="Trading & Finanzen"),
 "Game Dev": dict(en="Game Development", ar="تطوير الألعاب", fr="Développement de jeux", es="Desarrollo de juegos", de="Spieleentwicklung"),
 "No-code / Low-code": dict(en="No-code & Low-code", ar="بدون كود وكود منخفض", fr="No-code et low-code", es="No-code y low-code", de="No-Code & Low-Code"),
}
