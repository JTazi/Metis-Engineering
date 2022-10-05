# streamlit_app.py

import streamlit as st
import pymongo
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

mana_dict = {"Red":"R", "Blue":"U", "White":"W", "Black":"B", "Green":"G", "Colorless":""}
set_list = ['Strixhaven: School of Mages Minigames', 'Conspiracy', 'Magic 2013 Tokens', 'Zendikar Promos', 'Arena New Player Experience', 'Planar Chaos Promos', 'Iconic Masters Tokens', 'Conflux Tokens', 'Battle Royale Box Set', 'Planechase', 'MagicFest 2019', 'Modern Event Deck 2014 Tokens', 'Friday Night Magic 2003', 'Duel Decks: Jace vs. Vraska Tokens', 'Innistrad', 'Duel Decks Anthology: Divine vs. Demonic', 'Scars of Mirrodin Promos', 'Historic Anthology 3', 'Magic Origins Clash Pack', 'Betrayers of Kamigawa', 'Mystery Booster Playtest Cards 2021', 'Tarkir Dragonfury', 'Commander 2011 Oversized', 'Ravnica Allegiance', 'Commander 2014', 'Aether Revolt Promos', 'Journey into Nyx Promos', "Urza's Saga", 'Modern Horizons 2', 'Planeshift', 'Magic 2015 Clash Pack', 'Theros Tokens', 'Modern Horizons 2 Minigames', 'Junior APAC Series', 'Alchemy: Kamigawa', 'World Championship Decks 1998', 'RNA Ravnica Weekend', 'San Diego Comic-Con 2019', 'Future Sight Promos', 'Midnight Hunt Commander Display Commanders', 'Zendikar Rising Tokens', 'Duel Decks: Nissa vs. Ob Nixilis', 'Modern Horizons 2 Tokens', 'Commander 2013', 'Magic 2012', 'Zendikar Rising', 'Mythic Edition Tokens', 'Time Spiral Remastered', 'Ixalan Tokens', 'Rinascimento', 'Summer of Magic', 'Duel Decks: Mind vs. Might Tokens', 'Time Spiral Timeshifted', 'Duels of the Planeswalkers 2014 Promos ', 'New Capenna Commander', 'Return to Ravnica', 'Junior Super Series', 'Scars of Mirrodin', 'Avacyn Restored', 'Media Inserts', 'Eighth Edition', 'Duel Decks Anthology: Divine vs. Demonic Tokens', 'Modern Event Deck 2014', 'Dominaria United', 'Duel Decks: Knights vs. Dragons', 'Guru', 'Magic Player Rewards 2005', 'Store Championships 2022', 'Rise of the Eldrazi Promos', "Oversized 90's Promos", 'Modern Masters 2017', 'From the Vault: Relics', 'Innistrad: Double Feature', 'Innistrad: Midnight Hunt Promos', 'Exodus', 'Champions of Kamigawa Promos', 'Zendikar Rising Commander', 'Dominaria', 'Fifth Edition', 'Duel Decks: Venser vs. Koth', 'Masters 25 Tokens', 'Judge Gift Cards 2009', 'XLN Treasure Chest', 'Friday Night Magic 2009', 'Magic 2014 Promos', 'Mirrodin Besieged Tokens', 'Wizards Play Network 2021', '2017 Heroes of the Realm', 'Heads I Win, Tails You Lose', 'Forgotten Realms Commander Display Commanders', 'Collectors’ Edition', 'Magic 2010 Tokens', 'Kaldheim Minigames', 'Mirrodin', 'Premium Deck Series: Graveborn', 'Modern Horizons Tokens', 'Judge Gift Cards 2020', 'Modern Horizons 2 Art Series', 'Arabian Nights', 'Starter 1999', 'Visions', 'Judge Gift Cards 2012', 'Game Night 2019', 'Dragons of Tarkir Promos', 'Welcome Deck 2017', 'Ikoria: Lair of Behemoths', 'Coldsnap Theme Decks', 'Fourth Edition', 'Eternal Masters Tokens', 'Friday Night Magic 2012', 'Archenemy: Nicol Bolas Tokens', 'Kamigawa: Neon Dynasty Tokens', 'Battle for Zendikar Tokens', 'Duel Decks: Phyrexia vs. the Coalition', 'Morningtide Promos', 'Prophecy', 'Mercadian Masques Promos', "The Brothers' War", 'Eventide Tokens', 'Planar Chaos', "Commander Legends: Battle for Baldur's Gate", 'Masters Edition', 'Planeshift Promos', 'Planechase 2012', 'Duel Decks: Heroes vs. Monsters Tokens', 'Crimson Vow Art Series', 'Commander 2014 Tokens', 'Magic 2013 Promos', 'Kamigawa: Neon Destiny Minigames', 'Mystery Booster Playtest Cards 2019', 'Midnight Hunt Commander Tokens', 'Innistrad Tokens', 'IDW Comics 2013', 'Introductory Two-Player Set', 'Jumpstart Front Cards', 'From the Vault: Transform', 'Innistrad: Crimson Vow Tokens', 'Kaldheim', "Urza's Saga Promos", 'Friday Night Magic 2000', 'Judge Gift Cards 2001', 'Battlebond Tokens', 'Commander 2020 Oversized', 'Historic Anthology 1', 'Game Night 2022', 'Foreign Black Border', 'New Phyrexia Promos', 'World Championship Decks 2001', 'Tempest', 'Historic Anthology 5', 'Theros Promos', 'Gatecrash Tokens', 'Ixalan', 'Modern Horizons', 'From the Vault: Twenty', 'Forgotten Realms Commander', 'From the Vault: Legends', 'Judge Gift Cards 2006', 'Hour of Devastation', 'M20 Promo Packs', 'Unhinged Promos', "Alchemy Horizons: Baldur's Gate", 'Zendikar Rising Minigames', 'Shadowmoor', "Urza's Destiny", 'Magic Online Promos', 'Commander 2018', 'Wizards Play Network 2022', 'Sega Dreamcast Cards', 'Midnight Hunt Art Series', 'Friday Night Magic 2010', 'The List (Unfinity Foil Edition)', 'M19 Gift Pack', 'Eldritch Moon Promos', 'Lorwyn Tokens', 'Throne of Eldraine Promos', 'RNA Guild Kit Tokens', 'Arena League 2005', 'Gateway 2007', 'War of the Spark Promos', 'Magic Player Rewards 2001', 'Dominaria Tokens', 'Happy Holidays', 'Dominaria Remastered', 'Commander 2016', 'Adventures in the Forgotten Realms Tokens', 'GRN Ravnica Weekend', 'Conflux Promos', 'Duel Decks: Mirrodin Pure vs. New Phyrexia', 'Judge Gift Cards 2011', 'Warhammer 40,000', 'New Phyrexia', 'Commander 2017 Oversized', 'Ice Age', 'IDW Comics 2012', 'Invasion Promos', 'Historic Anthology 4', 'Kamigawa: Neon Dynasty Promos', 'Eventide', 'Amonkhet Remastered', 'Judgment', 'Duel Decks: Speed vs. Cunning', 'Commander 2014 Oversized', 'Wizards of the Coast Online Store', 'Mythic Edition', 'Duel Decks: Zendikar vs. Eldrazi', 'Commander 2016 Tokens', 'Magic 2013', 'Alara Reborn Tokens', 'Arena League 1996', 'Judge Gift Cards 2021', 'HarperPrism Book Promos', '2020 Heroes of the Realm', 'Planechase Anthology Tokens', 'Core Set 2021 Tokens', 'Friday Night Magic 2004', 'Gateway 2006', "Dragon's Maze Promos", 'Tenth Edition', 'Commander 2020 Tokens', 'Fate Reforged Promos', 'Judge Gift Cards 2016', "Battle for Baldur's Gate Promos", 'Born of the Gods Tokens', 'Magic 2012 Promos', 'Vintage Masters', 'Seventh Edition', 'Ixalan Promos', 'Archenemy: Nicol Bolas Schemes', 'Alliances', 'Judgment Promos', 'Warhammer 40,000 Tokens', "Battle for Baldur's Gate Art Series", 'Magic 2015 Tokens', "Journey into Nyx Hero's Path", 'Judge Gift Cards 2013', 'Masters Edition IV', 'Revised Edition', 'Invasion', 'Adventures in the Forgotten Realms Art Series', 'Unlimited Edition', 'Magic Player Rewards 2008', 'Magic Player Rewards 2007', 'Limited Edition Beta', 'Alara Reborn', 'Theros', 'Duel Decks: Elves vs. Goblins Tokens', 'Duel Decks Anthology: Elves vs. Goblins', 'Dominaria United Commander Tokens', 'Jumpstart', 'Duel Decks: Elves vs. Goblins', 'Innistrad: Crimson Vow Substitute Cards', 'Magic Premiere Shop 2010', 'Modern Masters 2015 Tokens', 'Friday Night Magic 2006', 'Magic Origins', 'Mirage', 'Fate Reforged Tokens', 'League Tokens 2017', 'Magic Origins Promos', 'World Championship Decks 2004', 'Commander Anthology Volume II', 'Modern Horizons Art Series', 'Morningtide Tokens', 'Friday Night Magic 2011', 'Lorwyn', 'Stronghold', 'Rise of the Eldrazi', 'Portal Second Age', 'Magic Player Rewards 2010', 'Kaldheim Commander', 'Wizards Play Network 2010', 'Khans of Tarkir Promos', "Commander's Arsenal", 'Theros Beyond Death Tokens', 'Unglued Tokens', 'Unglued', 'Core Set 2020 Tokens', 'Throne of Eldraine', 'Zendikar Rising Substitute Cards', 'Fate Reforged Clash Pack', 'Core Set 2020 Promos', 'Arena League 2006', 'Grand Prix Promos', 'Ninth Edition Promos', 'Duel Decks: Heroes vs. Monsters', 'Pioneer Challenger Decks 2022', 'Unstable Promos', 'Zendikar Expeditions', 'Guildpact', 'Shadowmoor Promos', 'Crimson Vow Commander Tokens', 'Exodus Promos', 'Unhinged', 'Core Set 2019 Tokens', 'Crimson Vow Commander', 'Shards of Alara', 'Shadows over Innistrad Promos', 'Neon Dynasty Art Series', '2019 Heroes of the Realm', 'Innistrad: Midnight Hunt Substitute Cards', 'Saviors of Kamigawa', 'Commander 2017', 'Signature Spellbook: Chandra', 'Scars of Mirrodin Tokens', 'Innistrad: Midnight Hunt', 'Judge Gift Cards 2010', 'New Capenna Commander Tokens', 'Ikoria: Lair of Behemoths Tokens', 'Oath of the Gatewatch Promos', 'Wizards Play Network 2009', 'Nemesis Promos', 'Salvat 2005', 'Wizards Play Network 2012', 'Dominaria United Commander', 'Kaladesh', 'Duel Decks: Elspeth vs. Tezzeret Tokens', 'Duel Decks: Garruk vs. Liliana', "Urza's Destiny Promos", 'Core Set 2021', 'League Tokens 2014', 'World Championship Decks 1999', 'Magic Premiere Shop 2005', 'Transformers', 'Commander 2020', 'From the Vault: Exiled', 'Magic Premiere Shop 2009', 'Mirrodin Besieged', 'Guilds of Ravnica Tokens', 'Conflux', 'Double Masters 2022 Tokens', 'Magic Player Rewards 2004', 'Duel Decks: Blessed vs. Cursed', 'Dark Ascension', 'Judge Gift Cards 2019', 'Avacyn Restored Tokens', 'Strixhaven: School of Mages Substitute Cards', 'Magic Player Rewards 2011', 'Innistrad Promos', 'Vintage Championship', 'Friday Night Magic 2001', 'Duel Decks Anthology: Jace vs. Chandra', 'Kaladesh Promos', 'Oath of the Gatewatch Tokens', 'Khans of Tarkir', 'Celebration Cards', 'World Championship Decks 2002', 'Explorers of Ixalan', 'Kaldheim Tokens', 'Commander Collection: Green', 'League Tokens 2016', 'New Capenna Art Series', 'Modern Horizons 1 Timeshifts', 'Khans of Tarkir Tokens', 'Game Night 2019 Tokens', 'Magic Premiere Shop 2008', 'Duel Decks: Mind vs. Might', 'Arena League 1999', 'Modern Horizons Promos', 'Future Sight', 'Unstable Tokens', 'Duel Decks: Elves vs. Inventors Tokens', 'MagicFest 2020', 'Weatherlight', 'Odyssey', 'Kaldheim Commander Tokens', 'Pro Tour Collector Set', 'Worldwake', '2017 Gift Pack', 'Lunar New Year 2018 ', 'Dominaria Promos', 'Starter Commander Decks', 'Oath of the Gatewatch', 'Modern Masters 2017 Tokens', 'Scourge', 'Judge Gift Cards 2007', 'Wizards Play Network 2008', 'Double Masters Tokens', 'Kaladesh Inventions', 'Time Spiral Promos', 'Streets of New Capenna', 'Magic 2015 Promos', 'World Championship Promos', 'Amonkhet Promos', 'Innistrad: Midnight Hunt Tokens', 'Duel Decks: Sorin vs. Tibalt', 'Magic 2015', 'Ultimate Masters', 'Arena New Player Experience Cards', 'Multiverse Gift Box', 'Magic 2012 Tokens', 'Arena League 2003', 'Duels of the Planeswalkers 2012 Promos ', 'Fourth Edition Foreign Black Border', 'Fifth Dawn Promos', 'Rivals of Ixalan Promos', 'Friday Night Magic 2002', 'Game Day Promos', 'Commander 2021 Display Commanders', 'Mirrodin Promos', "The Brothers' War Retro Artifacts", 'Betrayers of Kamigawa Promos', 'Kaldheim Promos', 'Explorer Anthology 1', 'HasCon 2017', 'M15 Prerelease Challenge', 'Modern Masters', 'Worldwake Promos', 'Apocalypse', 'Commander Collection: Black', 'Commander Anthology Volume II Tokens', 'Nationals Promos', 'Arena League 2001', 'Commander Anthology', 'San Diego Comic-Con 2016', 'Transformers Tokens', 'MicroProse Promos', 'Judge Gift Cards 2005', 'Unfinity Sticker Sheets', 'Antiquities', 'Duel Decks: Jace vs. Vraska', 'Shards of Alara Tokens', 'Dragon Con', 'World Championship Decks 2000', 'Duel Decks Anthology: Elves vs. Goblins Tokens', 'Born of the Gods', 'MagicFest 2021', 'Magic 2011', 'Modern Masters Tokens', 'Commander Legends', 'Strixhaven: School of Mages Tokens', 'Arena League 2000', 'Theros Beyond Death Promos', 'Kamigawa: Neon Dynasty Substitute Cards', 'Judge Gift Cards 2003', 'Rivals Quick Start Set', 'Champs and States', 'Miscellaneous Book Promos', 'Love Your LGS 2022', 'Strixhaven: School of Mages', 'Hachette UK', 'Aether Revolt Tokens', 'Aether Revolt', 'Dominaria United Art Series', 'Portal', 'Return to Ravnica Tokens', 'Year of the Tiger 2022', 'Duels of the Planeswalkers', 'Battle for Zendikar Promos', 'Friday Night Magic 2013', 'Astral Cards', 'Signature Spellbook: Gideon', 'Streets of New Capenna Minigames', 'Duel Decks: Divine vs. Demonic', 'Dragons of Tarkir', 'Darksteel', 'Historic Anthology 6', 'GRN Guild Kit', 'Deckmasters', 'From the Vault: Annihilation', 'World Championship Decks 2003', 'Fifth Dawn', 'Face the Hydra', 'Promotional Schemes', 'Legends', 'Coldsnap Promos', 'Ponies: The Galloping', 'Commander 2021', 'Renaissance', 'Defeat a God', "Born of the Gods Hero's Path", 'Duels of the Planeswalkers 2015 Promos ', 'From the Vault: Lore', 'Shards of Alara Promos', 'Commander Anthology Tokens', "Commander Legends: Battle for Baldur's Gate Minigames", 'Darksteel Promos', 'Battle for Zendikar', 'Eldritch Moon', 'Conspiracy Promos', 'Regional Championship Qualifiers 2022', 'Eternal Masters', 'Journey into Nyx', 'Eighth Edition Promos', 'Apocalypse Promos', 'Double Masters', 'Commander 2017 Tokens', 'URL/Convention Promos', 'Commander 2019', 'Ninth Edition', 'Global Series Jiang Yanggu & Mu Yanling', 'Judge Gift Cards 2014', 'Duel Decks: Ajani vs. Nicol Bolas', 'Vanguard Series', 'Arena New Player Experience Extras', 'Duel Decks: Merfolk vs. Goblins', 'GRN Guild Kit Tokens', 'IDW Comics 2014', 'Judge Gift Cards 2022', "Urza's Legacy", 'Onslaught', 'Lorwyn Promos', 'Alara Reborn Promos', 'Tenth Edition Promos', 'Magic Player Rewards 2003', 'Duel Decks: Venser vs. Koth Tokens', 'World Magic Cup Qualifiers', 'M19 Standard Showdown', 'Zendikar Rising Art Series', 'Commander 2015', 'Commander 2021 Tokens', 'Wizards Play Network 2011', 'Duels of the Planeswalkers 2013 Promos ', "Ugin's Fate", 'Friday Night Magic 2005', 'Game Night', 'Dominaria United Japanese Promo Tokens', 'Core Set 2021 Promos', 'Hour of Devastation Tokens', 'Gatecrash', 'Magic Online Theme Decks', 'Zendikar', 'Magic 2010', 'Eldritch Moon Tokens', 'Judge Gift Cards 2008', 'Friday Night Magic 2016', 'Rise of the Eldrazi Tokens', 'Magic Premiere Shop 2011', 'League Tokens 2015', 'Zendikar Rising Promos', 'Duel Decks Anthology: Garruk vs. Liliana', "Urza's Legacy Promos", 'Modern Masters 2015', 'Portal Three Kingdoms', 'Magic 2014 Tokens', 'Signature Spellbook: Jace', 'Dissension Promos', 'Innistrad: Crimson Vow Minigames', 'Nemesis', 'Rivals of Ixalan Tokens', 'Ravnica: City of Guilds', 'Dragons of Tarkir Tokens', 'San Diego Comic-Con 2017', 'War of the Spark Tokens', 'Portal: Three Kingdoms Promos', 'Judge Gift Cards 1998', 'Core Set 2019 Promos', 'Commander 2011', 'Unfinity Tokens', 'Conspiracy: Take the Crown Tokens', 'Magic 2011 Tokens', 'Judge Gift Cards 2018', '2018 Heroes of the Realm', 'Modern Horizons 2 Promos', 'Duel Decks: Phyrexia vs. the Coalition Tokens', 'Universes Within', 'Duels of the Planeswalkers 2009 Promos ', 'Archenemy Schemes', 'Commander 2018 Tokens', '30th Anniversary History Promos', 'Judge Gift Cards 2004', 'Zendikar Rising Expeditions', 'Duel Decks: Ajani vs. Nicol Bolas Tokens', 'Mystery Booster', 'Shadowmoor Tokens', 'Archenemy: Nicol Bolas', 'Commander 2011 Launch Party', 'Friday Night Magic 2014', 'Commander 2019 Oversized', 'Magic Player Rewards 2009', 'Duel Decks Anthology: Garruk vs. Liliana Tokens', 'DCI Legend Membership', 'Odyssey Promos', 'Friday Night Magic 2018', 'Homelands', 'Shadows over Innistrad Tokens', 'Zendikar Rising Commander Tokens', 'Duel Decks: Izzet vs. Golgari', 'Beatdown Box Set', 'Fate Reforged', "Dragon's Maze", 'Duel Decks: Elspeth vs. Kiora', 'Return to Ravnica Promos', 'Open the Helvault', 'Dark Ascension Tokens', 'Coldsnap', 'Arena Beginner Set', 'Theros Beyond Death', 'Ravnica Allegiance Tokens', 'The Dark', 'Unstable', 'Magic 2011 Promos', 'Neon Dynasty Commander Tokens', 'Duel Decks: Jace vs. Chandra', 'Dominaria United Tokens', 'Oversized League Prizes', 'Adventures in the Forgotten Realms Minigames', 'Hobby Japan Promos', 'Commander 2018 Oversized', 'Journey into Nyx Tokens', 'Rivals of Ixalan', 'Legacy Championship', 'Magic Player Rewards 2006', 'World Championship Decks 1997', 'Ultimate Masters Tokens', 'San Diego Comic-Con 2013', 'Guildpact Promos', 'Judge Gift Cards 2015', 'The List', '30th Anniversary Promos', 'Magic Premiere Shop 2006', 'Streets of New Capenna Promos', 'Legions Promos', 'Duel Decks: Jace vs. Chandra Tokens', 'XLN Standard Showdown', 'Mystery Booster Retail Edition Foils', 'Secret Lair: Ultimate Edition', 'Ikoria: Lair of Behemoths Promos', 'Kaladesh Remastered', 'Masters 25', 'Amonkhet', 'Secret Lair Drop', 'Tempest Remastered', 'Alchemy: Innistrad', 'Summer Vacation Promos 2022', 'Adventures in the Forgotten Realms', 'Archenemy', 'Arena League 2004', 'San Diego Comic-Con 2014', 'Morningtide', 'Unsanctioned', 'Planechase Anthology', 'Planechase Anthology Planes', 'Midnight Hunt Commander', 'Zendikar Tokens', 'Guilds of Ravnica', 'Duel Decks: Elspeth vs. Tezzeret', "The Brothers' War Commander", 'Guilds of Ravnica Promos', 'Innistrad: Crimson Vow Promos', 'Limited Edition Alpha', 'Friday Night Magic 2015', 'Junior Series Europe', 'Commander 2015 Oversized', 'Kaldheim Art Series', 'Resale Promos', 'Stronghold Promos', 'New Capenna Commander Promos', 'Scourge Promos', 'Dissension', 'Masters Edition III', 'Friday Night Magic 2008', 'Ultimate Box Topper', 'Streets of New Capenna Tokens', 'Tempest Promos', 'Prophecy Promos', '15th Anniversary Cards', 'Year of the Ox 2021', 'Amonkhet Invocations', 'Love Your LGS 2020', 'Starter 2000', 'Magic Player Rewards 2002', 'Kaladesh Tokens', 'Duel Decks Anthology: Jace vs. Chandra Tokens', 'Unsanctioned Tokens', 'Time Spiral Remastered Tokens', 'Salvat 2011', 'Historic Anthology 2', 'Planechase 2012 Planes', 'Jumpstart Arena Exclusives', 'San Diego Comic-Con 2015', 'New Phyrexia Tokens', "Dragon's Maze Tokens", 'Avacyn Restored Promos', 'Shadows over Innistrad', 'Intl. Collectors’ Edition', 'Fallen Empires', 'Planechase Planes', 'Duel Decks: Divine vs. Demonic Tokens', 'Promotional Planes', 'Commander 2016 Oversized', 'Japan Junior Tournament', 'Time Spiral', 'Unfinity', 'Battle the Horde', 'Duel Decks: Merfolk vs. Goblins Tokens', 'Streets of New Capenna Southeast Asia Tokens', 'Neon Dynasty Commander', 'From the Vault: Realms', 'Dark Ascension Promos', 'Pro Tour Promos', 'Judge Gift Cards 2000', 'Arena League 2002', 'Hour of Devastation Promos', 'Commander Legends Tokens', 'Double Masters 2022', 'Pioneer Challenger Decks 2021', 'Iconic Masters', 'Magic 2014', 'League Tokens 2012', 'Saviors of Kamigawa Promos', 'Kamigawa: Neon Dynasty', 'Gateway 2008', 'Strixhaven: School of Mages Promos', 'San Diego Comic-Con 2018', 'Conspiracy: Take the Crown', 'Judge Gift Cards 1999', 'Battlebond', 'Alchemy: New Capenna', 'Commander 2015 Tokens', '2016 Heroes of the Realm', 'Magic 2010 Promos', 'BFZ Standard Series', 'Torment Promos', 'Crimson Vow Commander Display Commanders', 'Legions', 'Onslaught Promos', 'Gatecrash Promos', 'Born of the Gods Promos', 'Jumpstart: Historic Horizons', 'Treasure Chest', 'Redemption Program', 'Champions of Kamigawa', 'Torment', 'Two-Headed Giant Tournament', 'Duel Decks: Sorin vs. Tibalt Tokens', 'Magic Online Avatars', 'Conspiracy Tokens', 'Ravnica: City of Guilds Promos', 'Legendary Cube Prize Pack', 'Amonkhet Tokens', 'Chronicles', 'Friday Night Magic 2007', 'Judge Gift Cards 2017', 'Eventide Promos', 'Mirrodin Besieged Promos', 'Ravnica Allegiance Promos', 'Duel Decks: Knights vs. Dragons Tokens', 'Duel Decks: Elves vs. Inventors', 'Magic Origins Tokens', 'From the Vault: Dragons', 'Duels of the Planeswalkers 2010 Promos ', 'Anthologies', "Commander's Arsenal Oversized", 'Core Set 2020', 'Friday Night Magic 2017', 'Premium Deck Series: Slivers', 'From the Vault: Angels', 'Throne of Eldraine Tokens', 'Duel Decks: Izzet vs. Golgari Tokens', 'Strixhaven Mystical Archive', 'Kaldheim Substitute Cards', 'Tenth Edition Tokens', 'RNA Guild Kit', 'Duel Decks: Garruk vs. Liliana Tokens', 'Summer Magic / Edgar', 'Love Your LGS 2021', 'Core Set 2019', 'Welcome Deck 2016', 'Premium Deck Series: Fire and Lightning', 'Judge Gift Cards 2002', 'Asia Pacific Land Program', 'Commander 2013 Oversized', 'War of the Spark', 'Classic Sixth Edition', 'Masters Edition II', 'Worldwake Tokens', 'Innistrad: Crimson Vow', 'European Land Program', 'League Tokens 2013', 'Dominaria United Promos', "Battle for Baldur's Gate Tokens", 'Adventures in the Forgotten Realms Promos', 'Strixhaven Art Series', 'Commander 2019 Tokens', "Theros Hero's Path", 'Magic Premiere Shop 2007', 'MTG Arena Promos', 'Battlebond Promos', 'Forgotten Realms Commander Tokens', 'Mercadian Masques']
keyword_url = 'https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_keywords'

#streamlit page config
st.set_page_config(
    layout="centered", page_icon='https://github.com/JTazi/Metis-Engineering/blob/901e6b1f820c12b29199ef635e835f4f2d395280/kisspng-magic-the-gathering-duels-of-the-planeswalker-magic-the-gathering-commander-5b1c8faf3cc9e6.955806671528598447249.png', page_title="MTG Table App"
)
st.title("MTG Table app")
st.write(
    """This app lets you sort and filter Magic the Gathering cards while also selecting a row for additional information"""
)

st.write("Go ahead, click on a row in the table below!")

#functions
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
	#**st.secrets["mongo"]
	return pymongo.MongoClient('mongodb+srv://jtaz:mtg123!!!@mtgcluster.yrodbby.mongodb.net/?retryWrites=true&w=majority')

client = init_connection()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=1200)
def get_table_data(set_list):
	db = client.mtg
	cursor = db.cards.find({'set_name':set_list}, {'_id':0, 'name':1, 'type_line':1, 'power':1,'toughness':1, 'rarity':1})
	table_data = list(cursor)  # make hashable for st.experimental_memo
	return table_data

@st.experimental_memo(ttl=600)  
def img_uri(card_name):
	db = client.mtg
	cursor = db.cards.find({'name':card_name},{'_id':0, 'image_uris':1})
	cur_list = list(cursor)
	image_uri = cur_list[0]['image_uris']['normal'] 
	return image_uri

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

#app code
# USer input on sidebar
set_select = st.sidebar.selectbox(
    "What set do you want to search?",
    (set_list)
)

st.sidebar.write(
    """For more information on keywords: [Keyword Wiki](keyword_url)"""
)

table_data = get_table_data(set_select)
df_table = pd.DataFrame(table_data)
		
selection = aggrid_interactive_table(df=df_table)

if selection:
	st.write("You selected:")
	card_name = selection["selected_rows"][0]['name']
	img_uri = img_uri(card_name)
	st.image(img_uri)
