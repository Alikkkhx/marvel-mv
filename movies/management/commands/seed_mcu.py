import os
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Phase, Movie

class Command(BaseCommand):
    help = 'Populates the database with ALL MCU movies from Phase 1 to Phase 6'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MCU Seeding...'))

        MOVIES = [
            # PHASE 1
            {
                "title": "Iron Man",
                "title_ru": "Железный человек",
                "year": 2008,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
                "description_en": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
                "description_ru": "Миллиардер-изобретатель Тони Старк попадает в плен к афганским террористам, где создает высокотехнологичный костюм-броню для побега и борьбы со злом.",
                "release_date": "2008-05-02",
                "director": "Jon Favreau"
            },
            {
                "title": "The Incredible Hulk",
                "title_ru": "Невероятный Халк",
                "year": 2008,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/gKzgy9j9igD6ls90vXm5zUCu558.jpg",
                "description_en": "Scientist Bruce Banner scours the planet for a cure to the unbridled force of rage within him: the Hulk.",
                "description_ru": "Брюс Беннер ищет лекарство от своего необычного «заболевания», превращающего его в неуправляемого зеленого гиганта во время эмоционального стресса.",
                "release_date": "2008-06-13",
                "director": "Louis Leterrier"
            },
            {
                "title": "Iron Man 2",
                "title_ru": "Железный человек 2",
                "year": 2010,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/6WBeUv4mUuTdc2H8QiOghj29nuG.jpg",
                "description_en": "With the world now aware of his identity as Iron Man, Tony Stark must contend with both his declining health and a vengeful madman.",
                "description_ru": "Мир узнал, что Тони Старк — это Железный человек. Теперь ему предстоит столкнуться с проблемами здоровья и новым опасным врагом из прошлого его семьи.",
                "release_date": "2010-05-07",
                "director": "Jon Favreau"
            },
            {
                "title": "Thor",
                "title_ru": "Тор",
                "year": 2011,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/prRk96pO3o6pST9BNoPb96pYp9v.jpg",
                "description_en": "The powerful, but arrogant god Thor is cast out of Asgard to live amongst humans on Earth, where he becomes one of their finest defenders.",
                "description_ru": "Высокомерный бог Тор изгнан из Асгарда на Землю в наказание за развязывание войны. Здесь он должен научиться смирению, чтобы вернуть свою силу.",
                "release_date": "2011-05-06",
                "director": "Kenneth Branagh"
            },
            {
                "title": "Captain America: The First Avenger",
                "title_ru": "Первый мститель",
                "year": 2011,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/vSNqiVGDmR076SbaS9H2mQKkOOt.jpg",
                "description_en": "Steve Rogers, a rejected military soldier, transforms into Captain America after taking a dose of a Super-Soldier serum.",
                "description_ru": "Хрупкий Стив Роджерс добровольно участвует в эксперименте, который превращает его в суперсолдата — Капитана Америка, символ надежды во время Второй мировой войны.",
                "release_date": "2011-07-22",
                "director": "Joe Johnston"
            },
            {
                "title": "The Avengers",
                "title_ru": "Мстители",
                "year": 2012,
                "phase": 1,
                "poster_url": "https://image.tmdb.org/t/p/w500/RYMX2uQBLChL8duOEsRCoff8o5.jpg",
                "description_en": "Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army.",
                "description_ru": "Ник Фьюри собирает команду супергероев, чтобы противостоять богу Локи и его инопланетной армии, угрожающей поработить Землю.",
                "release_date": "2012-05-04",
                "director": "Joss Whedon"
            },
            
            # PHASE 2
            {
                "title": "Iron Man 3",
                "title_ru": "Железный человек 3",
                "year": 2013,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/qhPtRWUnGwpnxC49SssVukvT9vC.jpg",
                "description_en": "When Tony Stark's world is pulled apart by a formidable terrorist called the Mandarin, he starts an odyssey of rebuilding and retribution.",
                "description_ru": "Тони Старк сталкивается с врагом, чей охват не знает границ. Когда его личный мир разрушен, он отправляется в мучительное путешествие, чтобы найти виновных.",
                "release_date": "2013-05-03",
                "director": "Shane Black"
            },
            {
                "title": "Thor: The Dark World",
                "title_ru": "Тор 2: Царство тьмы",
                "year": 2013,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/wp6D_pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "When the Dark Elves attempt to plunge the universe into darkness, Thor must embark on a perilous and personal journey that will reunite him with Jane Foster.",
                "description_ru": "Древняя инопланетная раса Темных Эльфов стремится погрузить вселенную во тьму. Тору предстоит объединиться с Локи, чтобы спасти девять миров.",
                "release_date": "2013-11-08",
                "director": "Alan Taylor"
            },
            {
                "title": "Captain America: The Winter Soldier",
                "title_ru": "Первый мститель: Другая война",
                "year": 2014,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/80VvVpSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "As Steve Rogers struggles to embrace his role in the modern world, he teams up with a fellow Avenger and S.H.I.E.L.D agent, Black Widow, to battle a new threat.",
                "description_ru": "Стив Роджерс объединяется с Наташей Романофф, чтобы раскрыть заговор внутри Щ.И.Т.а и противостоять таинственному убийце по прозвищу Зимний солдат.",
                "release_date": "2014-04-04",
                "director": "Anthony and Joe Russo"
            },
            {
                "title": "Guardians of the Galaxy",
                "title_ru": "Стражи Галактики",
                "year": 2014,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/r7D9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.",
                "description_ru": "Питер Квилл объединяется с группой отбросов общества, чтобы спасти галактику от фанатичного злодея Ронана, охотящегося за таинственной сферой.",
                "release_date": "2014-08-01",
                "director": "James Gunn"
            },
            {
                "title": "Avengers: Age of Ultron",
                "title_ru": "Мстители: Эра Альтрона",
                "year": 2015,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/t909pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "When Tony Stark and Bruce Banner try to jumpstart a dormant peacekeeping program called Ultron, things go horribly wrong and it's up to Earth's mightiest heroes to stop him.",
                "description_ru": "Попытка Тони Старка создать миротворческий искусственный интеллект оборачивается катастрофой. Мстители должны остановить Альтрона, решившего уничтожить человечество.",
                "release_date": "2015-05-01",
                "director": "Joss Whedon"
            },
            {
                "title": "Ant-Man",
                "title_ru": "Человек-муравей",
                "year": 2015,
                "phase": 2,
                "poster_url": "https://image.tmdb.org/t/p/w500/vG9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Armed with a super-suit with the astonishing ability to shrink in scale but increase in strength, cat burglar Scott Lang must help his mentor, Dr. Hank Pym.",
                "description_ru": "Вор Скотт Лэнг получает костюм, способный уменьшать его в размерах, но увеличивать силу. Ему предстоит помочь доктору Хэнку Пиму предотвратить глобальную угрозу.",
                "release_date": "2015-07-17",
                "director": "Peyton Reed"
            },

            # PHASE 3
            {
                "title": "Captain America: Civil War",
                "title_ru": "Первый мститель: Противостояние",
                "year": 2016,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/rAG2unY7C6W76SbaS9H2mQKkOOt.jpg",
                "description_en": "Political involvement in the Avengers' affairs causes a rift between Captain America and Iron Man.",
                "description_ru": "Закон о регистрации супергероев разделяет Мстителей на два лагеря под предводительством Капитана Америка и Железного человека.",
                "release_date": "2016-05-06",
                "director": "Anthony and Joe Russo"
            },
            {
                "title": "Doctor Strange",
                "title_ru": "Доктор Стрэндж",
                "year": 2016,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/u9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "After his career is destroyed, a brilliant but arrogant surgeon gets a new lease on life when a sorcerer takes him under her wing and trains him to defend the world against evil.",
                "description_ru": "Гениальный хирург Стивен Стрэндж теряет чувствительность рук после аварии. В поисках исцеления он открывает для себя мир магии и мистических искусств.",
                "release_date": "2016-11-04",
                "director": "Scott Derrickson"
            },
            {
                "title": "Guardians of the Galaxy Vol. 2",
                "title_ru": "Стражи Галактики. Часть 2",
                "year": 2017,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/y4pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father the ambitious celestial being Ego.",
                "description_ru": "Команда Стражей продолжает свои приключения в космосе, пока Питер Квилл узнает правду о своем происхождении и встречает своего настоящего отца.",
                "release_date": "2017-05-05",
                "director": "James Gunn"
            },
            {
                "title": "Spider-Man: Homecoming",
                "title_ru": "Человек-паук: Возвращение домой",
                "year": 2017,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/c2pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man, and finds himself on the trail of a new menace prowling the skies of New York City.",
                "description_ru": "Питер Паркер пытается совмещать жизнь обычного школьника и супергероя Человека-паука под присмотром наставника Тони Старка.",
                "release_date": "2017-07-07",
                "director": "Jon Watts"
            },
            {
                "title": "Thor: Ragnarok",
                "title_ru": "Тор: Рагнарёк",
                "year": 2017,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/o6pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarök, the destruction of his world, at the hands of the powerful and ruthless villain Hela.",
                "description_ru": "Тор лишается своего молота и оказывается в плену на другом конце вселенной. Он должен победить Халка в гладиаторском поединке и спасти Асгард от богини смерти Хелы.",
                "release_date": "2017-11-03",
                "director": "Taika Waititi"
            },
            {
                "title": "Black Panther",
                "title_ru": "Чёрная Пантера",
                "year": 2018,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/uxpSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "T'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country's past.",
                "description_ru": "Т’Чалла возвращается в изолированную африканскую страну Ваканду, чтобы занять престол. Но древний враг ставит под угрозу будущее не только Ваканды, но и всего мира.",
                "release_date": "2018-02-16",
                "director": "Ryan Coogler"
            },
            {
                "title": "Avengers: Infinity War",
                "title_ru": "Мстители: Война бесконечности",
                "year": 2018,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/7WsyChws3KyS09oUuRDbX0iUfNp.jpg",
                "description_en": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
                "description_ru": "Мстители и их союзники должны объединиться, чтобы остановить могущественного Таноса, прежде чем он соберет все Камни Бесконечности и уничтожит половину вселенной.",
                "release_date": "2018-04-27",
                "director": "Anthony and Joe Russo"
            },
            {
                "title": "Ant-Man and the Wasp",
                "title_ru": "Человек-муравей и Оса",
                "year": 2018,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/e9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "As Scott Lang balances being both a superhero and a father, Hope van Dyne and Dr. Hank Pym present an urgent new mission that finds the Ant-Man fighting alongside the Wasp to uncover secrets from their past.",
                "description_ru": "Скотт Лэнг пытается разобраться в последствиях своего выбора в пользу супергеройства. Но Хэнк Пим и Хоуп ван Дайн призывают его на новую миссию по спасению Джанет из квантового мира.",
                "release_date": "2018-07-06",
                "director": "Peyton Reed"
            },
            {
                "title": "Captain Marvel",
                "title_ru": "Капитан Марвел",
                "year": 2019,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/AtsgUekBbeFIpne29OOA6S7TIBp.jpg",
                "description_en": "Carol Danvers becomes one of the universe's most powerful heroes when Earth is caught in the middle of a galactic war between two alien races.",
                "description_ru": "Верс, воин расы Крии, оказывается на Земле 90-х годов. Здесь она вспоминает свое прошлое как Кэрол Денверс и становится величайшим защитником человечества.",
                "release_date": "2019-03-08",
                "director": "Anna Boden and Ryan Fleck"
            },
            {
                "title": "Avengers: Endgame",
                "title_ru": "Мстители: Финал",
                "year": 2019,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/or06vSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to restore balance to the universe.",
                "description_ru": "После щелчка Таноса выжившие Мстители должны найти способ вернуть павших друзей и восстановить порядок во вселенной, чего бы им это ни стоило.",
                "release_date": "2019-04-26",
                "director": "Anthony and Joe Russo"
            },
            {
                "title": "Spider-Man: Far From Home",
                "title_ru": "Человек-паук: Вдали от дома",
                "year": 2019,
                "phase": 3,
                "poster_url": "https://image.tmdb.org/t/p/w500/49pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever.",
                "description_ru": "Питер Паркер отправляется на каникулы в Европу, но отдых прерывается появлением таинственных элементалей и Ника Фьюри с новым заданием.",
                "release_date": "2019-07-02",
                "director": "Jon Watts"
            },

            # PHASE 4
            {
                "title": "Black Widow",
                "title_ru": "Чёрная Вдова",
                "year": 2021,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/q6pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.",
                "description_ru": "Наташе Романофф предстоит лицом к лицу встретиться со своим прошлым и шпионским наследием, чтобы разрушить заговор Красной комнаты.",
                "release_date": "2021-07-09",
                "director": "Cate Shortland"
            },
            {
                "title": "Shang-Chi and the Legend of the Ten Rings",
                "title_ru": "Шан-Чи и легенда десяти колец",
                "year": 2021,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/1pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Shang-Chi, the master of unarmed weaponry-based Kung Fu, is forced to confront his past after being drawn into the Ten Rings organization.",
                "description_ru": "Мастер боевых искусств Шан-Чи вынужден противостоять своему отцу и организации «Десять колец», из которой он пытался сбежать много лет назад.",
                "release_date": "2021-09-03",
                "director": "Destin Daniel Cretton"
            },
            {
                "title": "Eternals",
                "title_ru": "Вечные",
                "year": 2021,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/bcpSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "The saga of the Eternals, a race of immortal beings who lived on Earth and shaped its history and civilizations.",
                "description_ru": "Раса бессмертных существ, тайно живших на Земле тысячи лет, должна объединиться, чтобы защитить человечество от своих древних врагов — Девиантов.",
                "release_date": "2021-11-05",
                "director": "Chloé Zhao"
            },
            {
                "title": "Spider-Man: No Way Home",
                "title_ru": "Человек-паук: Нет пути домой",
                "year": 2021,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/1g0nxvSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
                "description_ru": "Личность Человека-паука раскрыта, и жизнь Питера Паркера превращается в хаос. Он просит Доктора Стрэнджа о помощи, но заклинание открывает разломы в мультивселенной.",
                "release_date": "2021-12-17",
                "director": "Jon Watts"
            },
            {
                "title": "Doctor Strange in the Multiverse of Madness",
                "title_ru": "Доктор Стрэндж: В мультивселенной безумия",
                "year": 2022,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Doctor Strange teams up with a mysterious teenage girl from his dreams who can travel across multiverses to battle multiple threats.",
                "description_ru": "Стивен Стрэндж отправляется в путешествие по мультивселенной вместе с юной Америкой Чавес, чтобы остановить могущественного врага, угрожающего всем мирам.",
                "release_date": "2022-05-06",
                "director": "Sam Raimi"
            },
            {
                "title": "Thor: Love and Thunder",
                "title_ru": "Тор: Любовь и гром",
                "year": 2022,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/p9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Thor enlists the help of Valkyrie, Korg and ex-girlfriend Jane Foster to fight Gorr the God Butcher, who intends to make the gods extinct.",
                "description_ru": "Тор ищет внутренний покой, но его отдых прерывает Горр Убийца Богов. Чтобы победить его, Тору нужна помощь Валькирии и Джейн Фостер, ставшей Могучим Тором.",
                "release_date": "2022-07-08",
                "director": "Taika Waititi"
            },
            {
                "title": "Black Panther: Wakanda Forever",
                "title_ru": "Чёрная Пантера: Ваканда навеки",
                "year": 2022,
                "phase": 4,
                "poster_url": "https://image.tmdb.org/t/p/w500/xpSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "The people of Wakanda fight to protect their home from intervening world powers as they mourn the death of King T'Challa.",
                "description_ru": "Королева Рамонда и Шури сражаются за будущее Ваканды после смерти Т’Чаллы. Им предстоит столкнуться с угрозой из глубин океана — Нэмором.",
                "release_date": "2022-11-11",
                "director": "Ryan Coogler"
            },

            # PHASE 5
            {
                "title": "Ant-Man and the Wasp: Quantumania",
                "title_ru": "Человек-муравей и Оса: Квантомания",
                "year": 2023,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/ngl9pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Scott Lang and Hope van Dyne, along with Hope's parents Hank Pym and Janet van Dyne, explore the Quantum Realm, where they interact with strange creatures and embark on an adventure that goes beyond the limits of what they thought was possible.",
                "description_ru": "Семья Скотта Лэнга попадает в Квантовый мир, где им предстоит столкнуться с Кангом Завоевателем — существом, способным управлять временем и пространством.",
                "release_date": "2023-02-17",
                "director": "Peyton Reed"
            },
            {
                "title": "Guardians of the Galaxy Vol. 3",
                "title_ru": "Стражи Галактики. Часть 3",
                "year": 2023,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/r2pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Still reeling from the loss of Gamora, Peter Quill rallies his team around him to defend the universe along with protecting one of their own.",
                "description_ru": "Питер Квилл должен сплотить Стражей для опасной миссии по спасению Ракеты. Это путешествие может стать последним для команды в ее нынешнем составе.",
                "release_date": "2023-05-05",
                "director": "James Gunn"
            },
            {
                "title": "The Marvels",
                "title_ru": "Марвелы",
                "year": 2023,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/9G0pSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Carol Danvers gets her powers entangled with those of Kamala Khan and Monica Rambeau, forcing them to work together to save the universe.",
                "description_ru": "Силы Кэрол Денверс, Камалы Хан и Моники Рамбо оказываются переплетены. Теперь при каждом использовании способностей они меняются местами в пространстве.",
                "release_date": "2023-11-10",
                "director": "Nia DaCosta"
            },
            {
                "title": "Deadpool & Wolverine",
                "title_ru": "Дэдпул и Росомаха",
                "year": 2024,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/8cdclpSff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Wolverine is recovering from his injuries when he crosses paths with the loudmouth Deadpool. They team up to defeat a common enemy.",
                "description_ru": "Дэдпулу предстоит объединиться с Росомахой из другой вселенной, чтобы спасти свой мир от уничтожения организацией TVA.",
                "release_date": "2024-07-26",
                "director": "Shawn Levy"
            },
            {
                "title": "Captain America: Brave New World",
                "title_ru": "Капитан Америка: Дивный новый мир",
                "year": 2025,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/6Sff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Sam Wilson, the new Captain America, finds himself in the middle of an international incident.",
                "description_ru": "Сэм Уилсон, принявший щит Капитана Америка, оказывается втянут в глобальный политический заговор и должен предотвратить мировую катастрофу.",
                "release_date": "2025-02-14",
                "director": "Julius Onah"
            },
            {
                "title": "Thunderbolts*",
                "title_ru": "Громовержцы*",
                "year": 2025,
                "phase": 5,
                "poster_url": "https://image.tmdb.org/t/p/w500/7Sff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "A group of anti-heroes goes on missions for the government.",
                "description_ru": "Команда бывших злодеев и антигероев собирается вместе для выполнения секретной миссии под руководством правительства.",
                "release_date": "2025-05-02",
                "director": "Jake Schreier"
            },

            # PHASE 6
            {
                "title": "The Fantastic Four: First Steps",
                "title_ru": "Фантастическая четвёрка: Первые шаги",
                "year": 2025,
                "phase": 6,
                "poster_url": "https://image.tmdb.org/t/p/w500/5Sff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "Marvel's First Family enters the MCU.",
                "description_ru": "Первая семья Марвел дебютирует в киновселенной, сталкиваясь с космическими угрозами в ретро-футуристичном стиле.",
                "release_date": "2025-07-25",
                "director": "Matt Shakman"
            },
            {
                "title": "Avengers: Doomsday",
                "title_ru": "Мстители: Судный день",
                "year": 2026,
                "phase": 6,
                "poster_url": "https://image.tmdb.org/t/p/w500/4Sff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "The Avengers face their ultimate challenge.",
                "description_ru": "Мстители вновь собираются вместе, чтобы противостоять новой глобальной угрозе — Доктору Думу.",
                "release_date": "2026-05-01",
                "director": "Anthony and Joe Russo"
            },
            {
                "title": "Avengers: Secret Wars",
                "title_ru": "Мстители: Секретные войны",
                "year": 2027,
                "phase": 6,
                "poster_url": "https://image.tmdb.org/t/p/w500/3Sff7vYp7vYp7vYp7vYp7v.jpg",
                "description_en": "The culmination of the Multiverse Saga.",
                "description_ru": "Грандиозный финал саги Мультивселенной, где столкнутся герои из всех реальностей.",
                "release_date": "2027-05-07",
                "director": "Anthony and Joe Russo"
            },
        ]

        def tmdb_w500(path: str) -> str:
            p = (path or "").lstrip("/")
            if not p:
                p = "78lPtwv72eTNqFW9COBYI0dWDJa.jpg"
            return f"https://image.tmdb.org/t/p/w500/{p}"

        # poster_path segments: must match the intended TMDb *movie id* (not a same-year title).
        # Fixed: Far From Home=429617 (567609 is Ready or Not), Brave New World=822119, Thunderbolts*=986056, FF=617126.
        TMDB_POSTER = {
            "Iron Man": "78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
            "The Incredible Hulk": "gKzYx79y0AQTL4UAk1cBQJ3nvrm.jpg",
            "Iron Man 2": "6WBeq4fCfn7AN0o21W9qNcRF2l9.jpg",
            "Thor": "prSfAi1xGrhLQNxVSUFh61xQ4Qy.jpg",
            "Captain America: The First Avenger": "vSNxAJTlD0r02V9sPYpOjqDZXUK.jpg",
            "The Avengers": "RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
            "Iron Man 3": "qhPtAc1TKbMPqNvcdXSOn9Bn7hZ.jpg",
            "Thor: The Dark World": "wp6OxE4poJ4G7c0U2ZIXasTSMR7.jpg",
            "Captain America: The Winter Soldier": "tVFRpFw3xTedgPGqxW0AOI8Qhh0.jpg",
            "Guardians of the Galaxy": "r7vmZjiyZw9rpJMQJdXpjgiCOk9.jpg",
            "Avengers: Age of Ultron": "4ssDuvEDkSArWEdyBl2X5EHvYKU.jpg",
            "Ant-Man": "rQRnQfUl3kfp78nCWq8Ks04vnq1.jpg",
            "Captain America: Civil War": "rAGiXaUfPzY7CDEyNKUofk3Kw2e.jpg",
            "Doctor Strange": "xf8PbyQcR5ucXErmZNzdKR0s8ya.jpg",
            "Guardians of the Galaxy Vol. 2": "y4MBh0EjBlMuOzv9axM4qJlmhzz.jpg",
            "Spider-Man: Homecoming": "c24sv2weTHPsmDa7jEMN0m2P3RT.jpg",
            "Thor: Ragnarok": "rzRwTcFvttcN1ZpX2xv4j3tSdJu.jpg",
            "Black Panther": "uxzzxijgPIY7slzFvMotPv8wjKA.jpg",
            "Avengers: Infinity War": "7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
            "Ant-Man and the Wasp": "cFQEO687n1K6umXbInzocxcnAQz.jpg",
            "Captain Marvel": "AtsgWhDnHTq68L0lLsUrCnM7TjG.jpg",
            "Avengers: Endgame": "ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
            "Spider-Man: Far From Home": "4q2NNj4S5dG2RLF9CpXsej7yXl.jpg",
            "Black Widow": "7JPpIjhD2V0sKyFvhB9khUMa30d.jpg",
            "Shang-Chi and the Legend of the Ten Rings": "9f2Q0U3IOsLgrI2HkvldwSABZy5.jpg",
            "Eternals": "lFByFSLV5WDJEv3KabbdAF959F2.jpg",
            "Spider-Man: No Way Home": "1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
            "Doctor Strange in the Multiverse of Madness": "ddJcSKbcp4rKZTmuyWaMhuwcfMz.jpg",
            "Thor: Love and Thunder": "pIkRyD18kl4FhoCNQuWxWu5cBLM.jpg",
            "Black Panther: Wakanda Forever": "sv1xJUazXeYqALzczSZ3O6nkH75.jpg",
            "Ant-Man and the Wasp: Quantumania": "qnqGbB22YJ7dSs4o6M7exTpNxPz.jpg",
            "Guardians of the Galaxy Vol. 3": "r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
            "The Marvels": "9GBhzXMFjgcZ3FdR9w3bUMMTps5.jpg",
            "Deadpool & Wolverine": "8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
            "Captain America: Brave New World": "pzIddUEMWhWzfvLI3TwxUG2wGoi.jpg",
            "Thunderbolts*": "hqcexYHbiTBfDIdDWxrxPtVndBX.jpg",
            "The Fantastic Four: First Steps": "pZPJsaFKWheTOerVhLnpP8TPp4B.jpg",
            "Avengers: Doomsday": "8HkIe2i4ScpCkcX9SzZ9IPasqWV.jpg",
            "Avengers: Secret Wars": "f0YBuh4hyiAheXhh4JnJWoKi9g5.jpg",
        }
        for row in MOVIES:
            name = row["title"]
            path = TMDB_POSTER.get(name)
            if not path and "poster_url" in row and row["poster_url"]:
                path = row["poster_url"].rstrip("/").split("/")[-1]
            row["poster_url"] = tmdb_w500(path or "")

        with transaction.atomic():
            # Create phases
            phases_objs = {}
            for i in range(1, 7):
                phase, created = Phase.objects.get_or_create(
                    name=f'Phase {i}',
                    defaults={'order': i}
                )
                phases_objs[i] = phase

            # Create movies
            for m_data in MOVIES:
                phase_num = m_data.pop('phase')
                phase_obj = phases_objs[phase_num]
                
                movie, created = Movie.objects.update_or_create(
                    title=m_data['title'],
                    defaults={
                        'title_ru': m_data['title_ru'],
                        'year': m_data['year'],
                        'phase': phase_obj,
                        'poster_url': m_data['poster_url'],
                        'description_en': m_data['description_en'],
                        'description_ru': m_data['description_ru'],
                        'release_date': date.fromisoformat(m_data['release_date']),
                        'director': m_data['director'],
                    }
                )
                
                if created:
                    self.stdout.write(f"Created: {movie.title}")
                else:
                    self.stdout.write(f"Updated: {movie.title}")

        self.stdout.write(self.style.SUCCESS('MCU Seeding Completed Successfully!'))
