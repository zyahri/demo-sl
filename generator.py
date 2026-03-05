import os
import re
import json
import urllib.parse
import random
import time
import requests

# ==========================================
# 1. FULL DATABASE (148 PRAGMATIC PLAY GAMES)
# ==========================================
GAMES_PRAGMATIC = [
    {"id": "vs20starlight", "name": "Starlight Princess", "rtp": "96.50%", "volatility": "High", "desc": "Star princess with a magic wand of winning multipliers."},
    {"id": "vs20starlightx", "name": "Starlight Princess 1000", "rtp": "96.50%", "volatility": "Very High", "desc": "Princess power upgraded up to x1000."},
    {"id": "vs20olympgate", "name": "Gates of Olympus", "rtp": "96.50%", "volatility": "High", "desc": "Grandpa Zeus awaits with x500 lightning."},
    {"id": "vs20olympx", "name": "Gates of Olympus 1000", "rtp": "96.50%", "volatility": "Very High", "desc": "Upgraded Zeus version with larger max win potential."},
    {"id": "vs20fruitsw", "name": "Sweet Bonanza", "rtp": "96.48%", "volatility": "Medium", "desc": "Colorful candy world with tumbling reels feature."},
    {"id": "vs20sbxmas", "name": "Sweet Bonanza Xmas", "rtp": "96.48%", "volatility": "Medium", "desc": "Christmas version of Sweet Bonanza with cold snow."},
    {"id": "vs20sugarrush", "name": "Sugar Rush", "rtp": "96.50%", "volatility": "High", "desc": "7x7 grid slot machine with sticky multiplier spots."},
    {"id": "vs20sugarrushx", "name": "Sugar Rush 1000", "rtp": "96.53%", "volatility": "Very High", "desc": "Extreme version of Sugar Rush with multipliers up to 1024x."},
    {"id": "vs20gatotkaca", "name": "Gates of Gatot Kaca", "rtp": "96.50%", "volatility": "High", "desc": "Indonesian superhero with mythological powers."},
    {"id": "vs20gatotkacax", "name": "Gates of Gatot Kaca 1000", "rtp": "96.50%", "volatility": "Very High", "desc": "Maximum power of the Indonesian superhero with x1000 multipliers."},
    {"id": "vs15zeushades", "name": "Zeus vs Hades - Gods of War", "rtp": "96.05%", "volatility": "Very High", "desc": "Choose your side in an epic battle between Zeus and Hades."},
    {"id": "vs20athena", "name": "Wisdom of Athena", "rtp": "96.07%", "volatility": "High", "desc": "Wisdom of goddess Athena with dynamic grid and multipliers."},
    {"id": "vs20forge", "name": "Forge of Olympus", "rtp": "96.25%", "volatility": "High", "desc": "Forge your victory with the blacksmith god of Olympus."},
    {"id": "vs5aztecgems", "name": "Aztec Gems", "rtp": "96.52%", "volatility": "Medium", "desc": "Classic 3x3 slot with an Aztec jungle theme."},
    {"id": "vs40wildwest", "name": "Wild West Gold", "rtp": "96.51%", "volatility": "High", "desc": "Wild west cowboys with sticky wilds in free spins."},
    {"id": "vs10bbsplash", "name": "Big Bass Splash", "rtp": "96.71%", "volatility": "High", "desc": "Fishing mania with fish money collection feature."},
    {"id": "vs20fruitparty", "name": "Fruit Party", "rtp": "96.47%", "volatility": "High", "desc": "Fruit party with random cluster multipliers."},
    {"id": "vs20goldfever", "name": "Gems Bonanza", "rtp": "96.51%", "volatility": "High", "desc": "Collect gems to trigger Gold Fever."},
    {"id": "vs20midas", "name": "The Hand of Midas", "rtp": "96.54%", "volatility": "High", "desc": "The golden touch of King Midas with sticky wilds."},
    {"id": "vswaysmadame", "name": "Madame Destiny Megaways", "rtp": "96.56%", "volatility": "High", "desc": "Fortune telling with the wheel of luck."},
    {"id": "vs20cleocatra", "name": "Cleocatra", "rtp": "96.20%", "volatility": "High", "desc": "Ancient Egyptian cats with sticky wilds."},
    {"id": "vs25mustang", "name": "Mustang Gold", "rtp": "96.53%", "volatility": "Medium-High", "desc": "Wild horses with Money Collect feature."},
    {"id": "vs25wolfgold", "name": "Wolf Gold", "rtp": "96.01%", "volatility": "Medium", "desc": "Golden wolf with Jackpot Respin feature."},
    {"id": "vs20mochimon", "name": "Mochimon", "rtp": "96.50%", "volatility": "High", "desc": "Cute mochi creatures with grid multipliers."},
    {"id": "vs20rabbit", "name": "Rabbit Garden", "rtp": "96.05%", "volatility": "High", "desc": "Rabbit garden with dropping coins feature."},
    {"id": "vs20knight", "name": "The Knight King", "rtp": "96.05%", "volatility": "High", "desc": "Knight king with mystical money symbols."},
    {"id": "vs20cowboy", "name": "Cowboy Coins", "rtp": "96.08%", "volatility": "High", "desc": "Cowboy duel collecting prize coins."},
    {"id": "vs20drghero", "name": "Dragon Hero", "rtp": "96.00%", "volatility": "High", "desc": "Dragon hero with super wilds."},
    {"id": "vs20stickybees", "name": "Sticky Bees", "rtp": "96.06%", "volatility": "High", "desc": "Honey bees leaving a trail of wilds."},
    {"id": "vs10adventure", "name": "Spirit of Adventure", "rtp": "96.60%", "volatility": "High", "desc": "Adventure to find ancient relics."},
    {"id": "vs50north", "name": "North Guardians", "rtp": "96.38%", "volatility": "High", "desc": "Northern guardians with mystical wild wheels."},
    {"id": "vs10firestrike2", "name": "Fire Strike 2", "rtp": "96.50%", "volatility": "Medium", "desc": "Classic burning fire jackpot."},
    {"id": "vs20starlightxmas", "name": "Starlight Christmas", "rtp": "96.50%", "volatility": "High", "desc": "Christmas edition of Starlight Princess."},
    {"id": "vs20shining", "name": "Shining Hot 100", "rtp": "96.32%", "volatility": "Medium", "desc": "Classic fruit slot with 100 paylines."},
    {"id": "vs20tropical", "name": "Tropical Tiki", "rtp": "96.43%", "volatility": "High", "desc": "Cluster wins on a tropical Tiki island."},
    {"id": "vs20bomb", "name": "Bomb Bonanza", "rtp": "96.46%", "volatility": "High", "desc": "Bomb explosion in a gold mine."},
    {"id": "vs20blackbull", "name": "Black Bull", "rtp": "96.51%", "volatility": "High", "desc": "Black bull collecting money coins."},
    {"id": "vs20greedy", "name": "Greedy Wolf", "rtp": "96.48%", "volatility": "High", "desc": "Greedy wolf chasing three little pigs."},
    {"id": "vs20striker", "name": "Octobeer Fortunes", "rtp": "96.53%", "volatility": "High", "desc": "Beer festival with cash prizes."},
    {"id": "vs20crown", "name": "Crown of Fire", "rtp": "96.36%", "volatility": "Medium", "desc": "Crown of fire burning the reels."},
    {"id": "vs20pirate", "name": "Pirate Golden Age", "rtp": "96.49%", "volatility": "High", "desc": "Golden age of treasure pirates."},
    {"id": "vs20aztec", "name": "Aztec Blaze", "rtp": "96.50%", "volatility": "High", "desc": "Aztec pyramids with giant symbols."},
    {"id": "vswaysmuertos", "name": "Muertos Multiplier Megaways", "rtp": "96.00%", "volatility": "High", "desc": "Mexican day of the dead with Megaways multipliers."},
    {"id": "vs20shield", "name": "Shield of Sparta", "rtp": "96.50%", "volatility": "High", "desc": "Spartan warfare with protective shields."},
    {"id": "vs20gems", "name": "Gems of Serengeti", "rtp": "96.40%", "volatility": "High", "desc": "Gemstones in the African wild."},
    {"id": "vs20snakes2", "name": "Snakes & Ladders Snake Eyes", "rtp": "96.08%", "volatility": "High", "desc": "Legendary snakes and ladders board game."},
    {"id": "vswaysodin", "name": "Fury of Odin Megaways", "rtp": "95.97%", "volatility": "High", "desc": "Wrath of god Odin on Megaways reels."},
    {"id": "vs20pizza", "name": "Pizza! Pizza? Pizza!", "rtp": "96.04%", "volatility": "High", "desc": "Delicious pizza slices with unique wins."},
    {"id": "vs20pinup", "name": "Pinup Girls", "rtp": "96.44%", "volatility": "High", "desc": "1950s retro pinup girls."},
    {"id": "vswaysmammoth", "name": "Mammoth Gold Megaways", "rtp": "96.03%", "volatility": "High", "desc": "Ice age mammoth with wild multipliers."},
    {"id": "vs20gods", "name": "Gods of Giza", "rtp": "96.01%", "volatility": "High", "desc": "Egyptian gods in an ancient labyrinth."},
    {"id": "vs20excalibur", "name": "Excalibur Unleashed", "rtp": "96.05%", "volatility": "High", "desc": "Legendary sword of King Arthur."},
    {"id": "vs20tundra", "name": "Tundra's Fortune", "rtp": "96.04%", "volatility": "High", "desc": "Luck in the icy Tundra fields."},
    {"id": "vs20fatpanda", "name": "Fat Panda", "rtp": "96.07%", "volatility": "High", "desc": "Cute panda with reel modifier features."},
    {"id": "vs20pve", "name": "Lamp of Infinity", "rtp": "96.07%", "volatility": "High", "desc": "Genie from the infinite magic lamp."},
    {"id": "vswaysheist", "name": "The Great Stick-Up", "rtp": "96.30%", "volatility": "High", "desc": "Detective heist with mystery symbols."},
    {"id": "vs20goblinheist", "name": "Goblin Heist PowerNudge", "rtp": "96.47%", "volatility": "High", "desc": "Goblin heist with PowerNudge mechanics."},
    {"id": "vs20jewels", "name": "Joker's Jewels", "rtp": "96.50%", "volatility": "Medium-High", "desc": "Simple classic Joker jewels."},
    {"id": "vs20kraken2", "name": "Release the Kraken 2", "rtp": "96.03%", "volatility": "High", "desc": "Deep sea monster attacks again."},
    {"id": "vs20fruitparty2", "name": "Fruit Party 2", "rtp": "96.53%", "volatility": "High", "desc": "Fruit party sequel with wild multipliers."},
    {"id": "vswaysdogs", "name": "The Dog House Megaways", "rtp": "96.55%", "volatility": "High", "desc": "Cute dogs on Megaways paths."},
    {"id": "vs20rhino", "name": "Great Rhino", "rtp": "96.53%", "volatility": "Medium", "desc": "Mighty rhino in the savanna."},
    {"id": "vs25wolfgoldx", "name": "Wolf Gold Ultimate", "rtp": "96.50%", "volatility": "High", "desc": "Ultimate version of Wolf Gold."},
    {"id": "vs20sugar1000", "name": "Sugar Rush 1000", "rtp": "96.53%", "volatility": "Very High", "desc": "Sugar Rush with thousands of multiplier potential."},
    {"id": "vs20candy", "name": "Candy Blitz", "rtp": "96.08%", "volatility": "High", "desc": "Sweet candy rush with multipliers."},
    {"id": "vs20floating", "name": "Floating Dragon Boat Festival", "rtp": "96.07%", "volatility": "High", "desc": "Lucky water dragon festival."},
    {"id": "vs20dice", "name": "Snakes & Ladders Megadice", "rtp": "96.68%", "volatility": "High", "desc": "Snakes and ladders with dice mechanics."},
    {"id": "vs20cleo", "name": "Eye of Cleopatra", "rtp": "96.50%", "volatility": "High", "desc": "Mysterious eye pattern of the Egyptian Queen."},
    {"id": "vs20wildhop", "name": "Wild Hop & Drop", "rtp": "96.46%", "volatility": "High", "desc": "Jumping frogs providing giant wilds."},
    {"id": "vs20octobeer", "name": "Octobeer Fortunes", "rtp": "96.53%", "volatility": "High", "desc": "Celebrate Oktoberfest with liquid wins."},
    {"id": "vs20firestrike", "name": "Fire Strike", "rtp": "96.50%", "volatility": "Medium", "desc": "Classic instant fire wins."},
    {"id": "vs20lucky", "name": "Lucky Grace & Charm", "rtp": "96.71%", "volatility": "High", "desc": "Viking female warriors searching for treasure."},
    {"id": "vs20hotburn", "name": "Hot to Burn", "rtp": "96.71%", "volatility": "Medium", "desc": "Burning classic retro fruits."},
    {"id": "vs20master", "name": "Master Joker", "rtp": "96.46%", "volatility": "High", "desc": "Single payline with wheel multipliers."},
    {"id": "vs20superx", "name": "Super X", "rtp": "96.51%", "volatility": "High", "desc": "Collect X symbols for bet multipliers."},
    {"id": "vs20santa", "name": "Santa's Wonderland", "rtp": "96.23%", "volatility": "High", "desc": "Colorful Santa's toy wonderland."},
    {"id": "vs20colossal", "name": "Colossal Cash Zone", "rtp": "96.50%", "volatility": "High", "desc": "Retro style colossal money zone."},
    {"id": "vs20queenie", "name": "Queenie", "rtp": "96.51%", "volatility": "High", "desc": "Queen of hearts from Alice in Wonderland."},
    {"id": "vs20drill", "name": "Drill That Gold", "rtp": "96.49%", "volatility": "High", "desc": "Underground gold miner dwarves."},
    {"id": "vs20clover", "name": "Clover Gold", "rtp": "96.54%", "volatility": "Medium", "desc": "Golden clover luck."},
    {"id": "vs20eyeofra", "name": "Eye of the Storm", "rtp": "96.71%", "volatility": "High", "desc": "Eye of the ancient Egyptian storm."},
    {"id": "vs20fishin", "name": "Fishin' Reels", "rtp": "96.50%", "volatility": "High", "desc": "Catch big fish under the sea."},
    {"id": "vs20temujin", "name": "Temujin Treasures", "rtp": "96.55%", "volatility": "High", "desc": "Wealth of Emperor Temujin."},
    {"id": "vs20wildboost", "name": "Wild Booster", "rtp": "96.47%", "volatility": "High", "desc": "Classic fruits with multiplier booster."},
    {"id": "vs20hotfiesta", "name": "Hot Fiesta", "rtp": "96.56%", "volatility": "High", "desc": "Festive Mexican street party."},
    {"id": "vs20elevator", "name": "Cash Elevator", "rtp": "96.64%", "volatility": "High", "desc": "Go up the elevator floors for bigger prizes."},
    {"id": "vs20panda2", "name": "Panda's Fortune 2", "rtp": "96.51%", "volatility": "High", "desc": "Lucky panda part two."},
    {"id": "vs20lightning", "name": "Lucky Lightning", "rtp": "96.45%", "volatility": "High", "desc": "Zeus's lightning bringing prizes."},
    {"id": "vs20heartrio", "name": "Heart of Rio", "rtp": "96.50%", "volatility": "Medium", "desc": "Exotic Rio de Janeiro carnival."},
    {"id": "vs20chicken", "name": "Chicken Drop", "rtp": "96.50%", "volatility": "High", "desc": "Golden chicken eggs bringing giant multipliers."},
    {"id": "vs20viking", "name": "Book of Vikings", "rtp": "96.50%", "volatility": "High", "desc": "Secret book of Viking warriors."},
    {"id": "vs20giza", "name": "Rise of Giza PowerNudge", "rtp": "96.49%", "volatility": "High", "desc": "Futuristic ancient Egypt with PowerNudge."},
    {"id": "vs20treasure", "name": "Treasure Wild", "rtp": "96.53%", "volatility": "High", "desc": "Collect gold coins in the treasure vault."},
    {"id": "vs20cashbonz", "name": "Cash Bonanza", "rtp": "96.52%", "volatility": "High", "desc": "Open the ever-growing money safe."},
    {"id": "vs20mystic", "name": "Mystic Chief", "rtp": "96.55%", "volatility": "High", "desc": "Indian chief with mystical powers."},
    {"id": "vs20piggy", "name": "Piggy Bank Bills", "rtp": "96.50%", "volatility": "High", "desc": "Combine the piggy bank bill pieces."},
    {"id": "vs20starpirate", "name": "Star Pirates Code", "rtp": "96.74%", "volatility": "High", "desc": "Space pirates searching for gems."},
    {"id": "vs20daydead", "name": "Day of Dead", "rtp": "96.49%", "volatility": "High", "desc": "Day of the dead celebration with walking wilds."},
    {"id": "vs20bigjuan", "name": "Big Juan", "rtp": "96.70%", "volatility": "High", "desc": "Big Juan Mexican party with jackpot bonus."},
    {"id": "vs20bounty", "name": "Bounty Gold", "rtp": "96.50%", "volatility": "High", "desc": "Fugitive cowboy with gold bounty."},
    {"id": "vs20smugglers", "name": "Smugglers Cove", "rtp": "96.50%", "volatility": "High", "desc": "Pirate treasure smuggler's cove."},
    {"id": "vs20crystal", "name": "Crystal Caverns", "rtp": "96.46%", "volatility": "High", "desc": "Crystal caverns with cascading multipliers."},
    {"id": "vs20depths", "name": "Wild Depths", "rtp": "96.48%", "volatility": "High", "desc": "Wildlife in the ocean depths."},
    {"id": "vs20secrets", "name": "Magician's Secrets", "rtp": "96.51%", "volatility": "High", "desc": "The Magician's magic wand secrets."},
    {"id": "vs20goldparty", "name": "Gold Party", "rtp": "96.50%", "volatility": "High", "desc": "Leprechaun's gold coin party."},
    {"id": "vs20valhalla", "name": "Gates of Valhalla", "rtp": "96.46%", "volatility": "High", "desc": "Heaven's gate of Nordic warriors."},
    {"id": "vs20rockvegas", "name": "Rock Vegas", "rtp": "96.64%", "volatility": "High", "desc": "Cavemen in a stone age casino."},
    {"id": "vs20tictac", "name": "Tic Tac Take", "rtp": "96.63%", "volatility": "High", "desc": "Modern neon Tic Tac Toe game."},
    {"id": "vs20rainbow", "name": "Rainbow Gold", "rtp": "96.63%", "volatility": "High", "desc": "Rainbow gold at the edge of the Leprechaun's world."},
    {"id": "vs20barn", "name": "Barn Festival", "rtp": "96.45%", "volatility": "High", "desc": "Harvest festival at the farm barn."},
    {"id": "vs20spirit", "name": "Spirit of Adventure", "rtp": "96.60%", "volatility": "High", "desc": "Jungle exploration to find relics."},
    {"id": "vs20clovergold", "name": "Clover Gold", "rtp": "96.54%", "volatility": "Medium", "desc": "Golden clover luck."},
    {"id": "vs20bull", "name": "Black Bull", "rtp": "96.51%", "volatility": "High", "desc": "Black bull collecting money prizes."},
    {"id": "vs20godsofgr", "name": "Gods of Giza", "rtp": "96.01%", "volatility": "High", "desc": "Egyptian gods on a collapsing grid."},
    {"id": "vs20aztecbl", "name": "Aztec Blaze", "rtp": "96.50%", "volatility": "High", "desc": "Giant symbols in the Aztec civilization."},
    {"id": "vs20tower", "name": "Towering Fortunes", "rtp": "96.50%", "volatility": "High", "desc": "Skyscrapers with high prizes."},
    {"id": "vs20granny", "name": "Granny's Attic", "rtp": "96.50%", "volatility": "High", "desc": "Treasure in grandma's attic."},
    {"id": "vs20voodoomagic", "name": "Voodoo Magic", "rtp": "96.50%", "volatility": "High", "desc": "Voodoo ritual bringing victory."},
    {"id": "vs20congo", "name": "Congo Cash", "rtp": "96.51%", "volatility": "High", "desc": "Congo jungle with upper prize board."},
    {"id": "vs20mysticchief", "name": "Mystic Chief", "rtp": "96.55%", "volatility": "High", "desc": "Tribal chief with expanding wilds."},
    {"id": "vs20temujintreas", "name": "Temujin Treasures", "rtp": "96.55%", "volatility": "High", "desc": "Wealth of the Mongol Conqueror."},
    {"id": "vs20luckygrace", "name": "Lucky Grace & Charm", "rtp": "96.71%", "volatility": "High", "desc": "Beautiful female Viking adventure."},
    {"id": "vs20emptybank", "name": "Empty the Bank", "rtp": "96.48%", "volatility": "High", "desc": "Bank heist with hold & respin feature."},
    {"id": "vs20chickenchase", "name": "Chicken Chase", "rtp": "96.48%", "volatility": "Low", "desc": "Chase chickens on the farm for a bonus."},
    {"id": "vs20drillgold", "name": "Drill That Gold", "rtp": "96.49%", "volatility": "High", "desc": "Underground gold mine drilling."},
    {"id": "vs20wildbeach", "name": "Wild Beach Party", "rtp": "96.53%", "volatility": "High", "desc": "Beach party with anime fruits."},
    {"id": "vs20goblin", "name": "Goblin Heist", "rtp": "96.47%", "volatility": "High", "desc": "Goblin stealing gold coins."},
    {"id": "vs20furyodin", "name": "Fury of Odin", "rtp": "95.97%", "volatility": "High", "desc": "Wrath of Odin on the battlefield."},
    {"id": "vs20mammoth", "name": "Mammoth Gold", "rtp": "96.03%", "volatility": "High", "desc": "Ancient Mammoth elephant producing gold."},
    {"id": "vs20pizza2", "name": "Pizza Pizza Pizza", "rtp": "96.04%", "volatility": "High", "desc": "Abundant Italian pizza serving."},
    {"id": "vs20fishingslots", "name": "Fishing Slots", "rtp": "96.50%", "volatility": "High", "desc": "Fishing in the prize pool."},
    {"id": "vs20wolfgoldultimate", "name": "Wolf Gold Ultimate", "rtp": "96.50%", "volatility": "High", "desc": "Final edition of Wolf Gold."},
    {"id": "vs20bbbonanza", "name": "Big Bass Bonanza", "rtp": "96.71%", "volatility": "Medium", "desc": "Fishing mania for cash prize fish."},
    {"id": "vs20bbkeep", "name": "Big Bass Keeping It Reel", "rtp": "96.07%", "volatility": "High", "desc": "Net big fish in the sea."},
    {"id": "vs20bbextreme", "name": "Big Bass Amazon Xtreme", "rtp": "96.07%", "volatility": "High", "desc": "Extreme fishing in the Amazon river."},
    {"id": "vs20bbfloats", "name": "Big Bass Day at the Races", "rtp": "96.07%", "volatility": "High", "desc": "Fisherman going to the horse races."},
    {"id": "vs20bbsecrets", "name": "Big Bass Secrets of the Lake", "rtp": "96.07%", "volatility": "High", "desc": "Secrets of the fish in the hidden lake."},
    {"id": "vs20bbfish", "name": "Big Bass Mission Fishin", "rtp": "96.07%", "volatility": "High", "desc": "Secret mission fishing for golden fish."},
    {"id": "vs20bbvegas", "name": "Big Bass Vegas Double Down Deluxe", "rtp": "96.07%", "volatility": "High", "desc": "Fishing in glittering Las Vegas."},
    {"id": "vs20candyorush", "name": "Candy Rush", "rtp": "96.50%", "volatility": "High", "desc": "Colorful candy rush."},
    {"id": "vs20fruitburst", "name": "Fruit Burst", "rtp": "96.40%", "volatility": "Medium", "desc": "Classic fresh fruit burst."},
    {"id": "vs20diamondstrike", "name": "Diamond Strike", "rtp": "96.48%", "volatility": "Medium", "desc": "Diamond gem lightning strike."},
    {"id": "vs20wildwestg", "name": "Wild West Gold", "rtp": "96.51%", "volatility": "High", "desc": "Gold in the wild west."},
    {"id": "vs20wwgmegaways", "name": "Wild West Gold Megaways", "rtp": "96.44%", "volatility": "High", "desc": "Cowboys in thousands of winning ways."},
    {"id": "vs20bonanzagold", "name": "Bonanza Gold", "rtp": "96.49%", "volatility": "High", "desc": "Gold mine full of gems."},
    {"id": "vs20pyramid", "name": "Pyramid Bonanza", "rtp": "96.48%", "volatility": "High", "desc": "Egyptian pyramid treasure."},
    {"id": "vs20doghouse", "name": "The Dog House", "rtp": "96.51%", "volatility": "High", "desc": "Dog house full of wild multipliers."},
    {"id": "vs20doghousem", "name": "The Dog House Megaways", "rtp": "96.55%", "volatility": "High", "desc": "Dog house Megaways paths."},
    {"id": "vs20doghousemh", "name": "The Dog House Multihold", "rtp": "96.06%", "volatility": "High", "desc": "Play multiple dog house screens."},
    {"id": "vs20fruitp", "name": "Fruit Party", "rtp": "96.47%", "volatility": "High", "desc": "Dropping cluster fruit party."},
    {"id": "vs20juicy", "name": "Juicy Fruits", "rtp": "96.52%", "volatility": "High", "desc": "Juicy fruits with giant wilds."},
    {"id": "vs20juicyly", "name": "Juicy Fruits Multihold", "rtp": "96.04%", "volatility": "High", "desc": "Juicy fruits on multiple reels."},
    {"id": "vs20aztecgd", "name": "Aztec Gems Deluxe", "rtp": "96.50%", "volatility": "High", "desc": "Deluxe edition of Aztec gems."},
    {"id": "vs20grtrhinom", "name": "Great Rhino Megaways", "rtp": "96.58%", "volatility": "High", "desc": "Giant rhino Megaways."},
    {"id": "vs20bufking", "name": "Buffalo King", "rtp": "96.06%", "volatility": "High", "desc": "Buffalo king in the meadow."},
    {"id": "vs20bufkingm", "name": "Buffalo King Megaways", "rtp": "96.52%", "volatility": "High", "desc": "Buffalo King in thousands of paths."},
    {"id": "vs20bufkingx", "name": "Buffalo King Untamed Megaways", "rtp": "96.02%", "volatility": "High", "desc": "Untamed Buffalo King."},
    {"id": "vs20madamem", "name": "Madame Destiny Megaways", "rtp": "96.56%", "volatility": "High", "desc": "Fate in Megaways paths."},
    {"id": "vs20mightytrex", "name": "Mighty Munching Munchkins", "rtp": "96.50%", "volatility": "Medium", "desc": "Hungry little creatures."},
    {"id": "vs20zombie", "name": "Zombie Carnival", "rtp": "96.50%", "volatility": "High", "desc": "Zombie carnival."},
    {"id": "vs20panda", "name": "Mahjong Panda", "rtp": "96.48%", "volatility": "High", "desc": "Panda playing Mahjong."},
    {"id": "vs20drillgold2", "name": "Drill That Gold", "rtp": "96.49%", "volatility": "High", "desc": "Dig gold to the bottom."},
    {"id": "vs20barnfest", "name": "Barn Festival", "rtp": "96.45%", "volatility": "High", "desc": "Barn harvest festival."},
    {"id": "vs20goldparty2", "name": "Gold Party", "rtp": "96.50%", "volatility": "High", "desc": "Lucky gold party."},
    {"id": "vs20magics", "name": "Magician's Secrets", "rtp": "96.51%", "volatility": "High", "desc": "The Magician's secrets."},
    {"id": "vs20crystalcav", "name": "Crystal Caverns Megaways", "rtp": "96.46%", "volatility": "High", "desc": "Crystal caverns Megaways."},
    {"id": "vs20superx2", "name": "Super X", "rtp": "96.51%", "volatility": "High", "desc": "Super X multiplier."},
    {"id": "vs20dayofdead", "name": "Day of Dead", "rtp": "96.49%", "volatility": "High", "desc": "Mexican day of the dead."},
    {"id": "vs20riseofgiza", "name": "Rise of Giza", "rtp": "96.49%", "volatility": "High", "desc": "Rise of futuristic Giza."},
    {"id": "vs20chickend", "name": "Chicken Drop", "rtp": "96.50%", "volatility": "High", "desc": "Golden egg chicken."},
    {"id": "vs20luckylight", "name": "Lucky Lightning", "rtp": "96.45%", "volatility": "High", "desc": "Lucky lightning."},
    {"id": "vs20pandasf2", "name": "Panda's Fortune 2", "rtp": "96.51%", "volatility": "High", "desc": "Panda's fortune 2."},
    {"id": "vs20cashelev", "name": "Cash Elevator", "rtp": "96.64%", "volatility": "High", "desc": "Cash elevator."},
    {"id": "vs20hotfiesta2", "name": "Hot Fiesta", "rtp": "96.56%", "volatility": "High", "desc": "Hot street party."},
    {"id": "vs20hothold2", "name": "Hot to Burn Hold and Spin", "rtp": "96.70%", "volatility": "High", "desc": "Classic fruit hold & spin."},
    {"id": "vs20congocash", "name": "Congo Cash", "rtp": "96.51%", "volatility": "Medium-High", "desc": "Wild Congo jungle."},
    {"id": "vs20johnhunter", "name": "John Hunter Mayan Gods", "rtp": "96.51%", "volatility": "High", "desc": "John Hunter in the Mayan Tribe."},
    {"id": "vs20spartanking", "name": "Spartan King", "rtp": "96.60%", "volatility": "High", "desc": "Spartan warlord."},
    {"id": "vs20bookofking", "name": "Book of Kingdoms", "rtp": "96.69%", "volatility": "Medium", "desc": "Explorer's book of kingdoms."},
    {"id": "vs20returnofdead", "name": "Return of the Dead", "rtp": "96.71%", "volatility": "High", "desc": "Resurrection of the Egyptian dead."},
    {"id": "vs20emerald", "name": "Emerald King", "rtp": "96.51%", "volatility": "High", "desc": "Leprechaun Emerald King."},
    {"id": "vs20wildwalker", "name": "Wild Walker", "rtp": "96.09%", "volatility": "High", "desc": "Wild walking zombies."},
    {"id": "vs20curseofwere", "name": "Curse of the Werewolf", "rtp": "96.50%", "volatility": "High", "desc": "Curse of the Werewolf."},
    {"id": "vs20peaky", "name": "Peaky Blinders", "rtp": "96.50%", "volatility": "High", "desc": "Official Peaky Blinders gang."},
    {"id": "vs20jungle", "name": "Jungle Gorilla", "rtp": "96.57%", "volatility": "Medium", "desc": "Lush jungle gorilla."},
    {"id": "vs20streetrace", "name": "Street Racer", "rtp": "96.52%", "volatility": "High", "desc": "Street wild racing."},
    {"id": "vs20drago", "name": "Drago Jewels of Fortune", "rtp": "96.50%", "volatility": "High", "desc": "Lucky dragon gems."},
    {"id": "vs20starz", "name": "Starz Megaways", "rtp": "96.48%", "volatility": "High", "desc": "Megaways galaxy stars."},
    {"id": "vs20hotburnx", "name": "Hot to Burn", "rtp": "96.71%", "volatility": "Medium", "desc": "Burning classic fruits."},
    {"id": "vs20fruitrainbow", "name": "Fruit Rainbow", "rtp": "96.53%", "volatility": "High", "desc": "Colorful fruit rainbow."},
    {"id": "vs20goldrush", "name": "Gold Rush", "rtp": "96.50%", "volatility": "Medium-High", "desc": "Dig gold in the mine."},
    {"id": "vs20888gold", "name": "888 Gold", "rtp": "97.52%", "volatility": "Medium", "desc": "Lucky number 888."},
    {"id": "vs20irish", "name": "Irish Charms", "rtp": "96.96%", "volatility": "Low", "desc": "Classic Irish charms."},
    {"id": "vs20diamonds", "name": "Diamonds are Forever", "rtp": "96.96%", "volatility": "Low", "desc": "Eternal diamond gems."},
    {"id": "vs20monkey", "name": "Monkey Madness", "rtp": "96.53%", "volatility": "Medium", "desc": "Crazy jungle monkeys."},
    {"id": "vs20fire88", "name": "Fire 88", "rtp": "96.46%", "volatility": "Medium", "desc": "Fire dragon number 88."},
    {"id": "vs20triple", "name": "Triple Tigers", "rtp": "97.52%", "volatility": "Medium", "desc": "Three lucky tigers."},
    {"id": "vs205lions", "name": "5 Lions", "rtp": "96.50%", "volatility": "High", "desc": "Five Asian golden lions."},
    {"id": "vs205lionsg", "name": "5 Lions Gold", "rtp": "96.50%", "volatility": "High", "desc": "Golden lions with jackpot."},
    {"id": "vs205lionsm", "name": "5 Lions Megaways", "rtp": "96.50%", "volatility": "High", "desc": "Golden lions in Megaways."},
    {"id": "vs20chilli", "name": "Chilli Heat", "rtp": "96.50%", "volatility": "Medium", "desc": "Spicy Mexican chilli."},
    {"id": "vs20chillim", "name": "Chilli Heat Megaways", "rtp": "96.50%", "volatility": "High", "desc": "Spicy chilli in Megaways."}
]

# ==========================================
# 2. GA4 MAPPING CONFIGURATION
# ==========================================
# Masukkan ID Measurement Google Analytics Anda di sini untuk domain Anda
GA_MAPPING = {
    "https://domain-utama-anda.com": "G-XXXXXXXXXX", 
    "http://127.0.0.1:5500": "G-XXXXXXXXXX" # Jika Anda tes di lokal
}

# ==========================================
# 3. DOMAIN CONFIGURATION (SINGLE DOMAIN)
# ==========================================
TARGETS = [
    {
        "domain": "http://127.0.0.1:5500", # Ganti dengan nama domain utama Anda saat live
        "path": ".", # <-- Menyimpan hasil render HTML di folder saat ini (atau ganti ke folder spesifik)
        "site_title": "Pragmatic Demo Pro",
        "provider_name": "Pragmatic Play",
        "database": GAMES_PRAGMATIC,
        "accent_color": "#e50914",
        "backlink_url": "https://situs-utama-anda.com/ref"
    }
]

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
def slugify(text):
    text = str(text).lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def ping_new_content(title, url):
    """Pings services to notify search engines of new content."""
    try:
        services = {'title': title, 'blogurl': url, 'chk_weblogscom': 'on', 'chk_blogs': 'on', 'chk_google': 'on'}
        requests.get("http://pingomatic.com/ping/", params=services, timeout=2)
    except:
        pass

def generate_sitemap(target_path, site_domain, folder_name="game"):
    full_path = os.path.join(target_path, folder_name)
    if not os.path.exists(full_path): return
    print(f"    🗺️  Generating sitemap for {folder_name}...")
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    files = [f for f in os.listdir(full_path) if f.endswith('.html')]
    for filename in files:
        file_path = os.path.join(full_path, filename)
        mod_time = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(file_path)))
        xml_content += f'  <url>\n    <loc>{site_domain}/{folder_name}/{filename}</loc>\n    <lastmod>{mod_time}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
    xml_content += '</urlset>'
    with open(os.path.join(target_path, f"{folder_name}_sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(xml_content)

def generate_master_sitemap(target_path, site_domain):
    today = time.strftime('%Y-%m-%d')
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml_content += f'  <sitemap>\n    <loc>{site_domain}/game_sitemap.xml</loc>\n    <lastmod>{today}</lastmod>\n  </sitemap>\n'
    xml_content += '</sitemapindex>'
    with open(os.path.join(target_path, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(xml_content)

def generate_robots_txt(target_path, site_domain):
    print("    🤖 Generating robots.txt...")
    content = f"""User-agent: *
Allow: /
Disallow: /*?search=
Disallow: /*&search=
Disallow: /*?lang=
Disallow: /*&lang=
Sitemap: {site_domain}/sitemap.xml
"""
    with open(os.path.join(target_path, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(content)

# ==========================================
# 5. MAIN ENGINE
# ==========================================
def generate_play_pages():
    print("🎬 Starting Execution of Static Generator (Single Domain)...")
    start_time = time.time()
    
    # 1. Ensure template_play.html is available
    try:
        with open('template_play.html', 'r', encoding='utf-8') as f: 
            TEMPLATE_PLAY = f.read()
    except FileNotFoundError:
        print("❌ CRITICAL ERROR: template_play.html not found in the master folder!")
        return

    # 2. Execute target domain
    for target in TARGETS:
        domain_url = target['domain'].rstrip('/')
        root_path = target['path']
        provider_name = target['provider_name']
        game_db = target['database']
        
        # --- LOGIKA GA4 INJECTION ---
        analytics_code = ""
        if domain_url in GA_MAPPING:
            ga_id = GA_MAPPING[domain_url]
            analytics_code = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{ga_id}');</script>"""
        # ----------------------------

        print(f"\n🚀 Processing {len(game_db)} Game Pages for: {domain_url}")
        
        # Membuat direktori (path lokal) secara otomatis jika belum ada
        if not os.path.exists(root_path):
            os.makedirs(root_path, exist_ok=True)
            
        # Create 'game' folder if it doesn't exist
        game_dir = os.path.join(root_path, "game")
        os.makedirs(game_dir, exist_ok=True)
        
        generated_count = 0
        
        # 3. Execute file creation per game
        for game in game_db:
            slug = slugify(game['name'])
            output_filename = f"{slug}.html"
            output_path = os.path.join(game_dir, output_filename)
            
            # --- CEK FILE LAMA ---
            if os.path.exists(output_path):
                continue
            
            # Automatic formulation of Pragmatic Iframe URL
            iframe_url = f"https://demogamesfree.pragmaticplay.net/gs2c/openGame.do?gameSymbol={game['id']}&websiteUrl=https%3A%2F%2Fdemogamesfree.pragmaticplay.net&jurisdiction=99&lobby_url=https%3A%2F%2Fwww.pragmaticplay.com%2Fen%2F&lang=en&cur=USD"
            
            # Simplified Canonical & Page URL
            canonical_url = f"{domain_url}/game/{output_filename}"
            page_url = f"{domain_url}/game/{output_filename}"
            
            # --- A. BACKGROUND IMAGE AND BING PROXY POSTER LOGIC ---
            search_query_bg = f"{provider_name} {game['name']} cinematic wallpaper hd"
            proxy_bg_url = f"https://tse2.mm.bing.net/th?q={urllib.parse.quote(search_query_bg)}&w=1920&h=1080&c=7&rs=1&p=0&dpr=1&pid=1.7"
            
            search_query_poster = f"{provider_name} {game['name']} slot poster"
            proxy_poster_url = f"https://tse2.mm.bing.net/th?q={urllib.parse.quote(search_query_poster)}&w=400&h=600&c=7&rs=1&p=0&dpr=1&pid=1.7"
            
            # --- B. RECOMMENDATION SLIDER LOGIC ---
            related_html = ""
            available_for_random = [g for g in game_db if g['id'] != game['id']]
            random_related = random.sample(available_for_random, min(15, len(available_for_random)))
            
            for r_game in random_related:
                r_slug = slugify(r_game['name'])
                r_query = f"{provider_name} {r_game['name']} slot poster"
                r_img = f"https://tse2.mm.bing.net/th?q={urllib.parse.quote(r_query)}&w=400&h=600&c=7&rs=1&p=0&dpr=1&pid=1.7"
                fallback_url = f"https://placehold.co/400x600/141519/e50914?font=Montserrat&text={urllib.parse.quote(r_game['name'])}"
                random_rating = round(random.uniform(6.0, 9.5), 1)
                
                related_html += f"""
                <a href="{r_slug}.html" class="game-card">
                    <div class="game-card-thumb">
                        <div class="top-badges">
                            <div class="heart-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg></div>
                            <div class="rating-badge">★ {random_rating}</div>
                        </div>
                        <img src="{r_img}" alt="{r_game['name']}" onerror="this.onerror=null; this.src='{fallback_url}';">
                    </div>
                    <div class="game-card-info">
                        <h3>{r_game['name']}</h3>
                        <div class="provider-tag">2026 • {provider_name}</div>
                    </div>
                </a>
                """

            # --- C. SCHEMA.ORG LOGIC (SEO) ---
            schema_data = {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": game['name'] + " Demo",
                "description": game['desc'],
                "image": proxy_poster_url,
                "url": canonical_url,
                "author": {"@type": "Organization", "name": provider_name},
                "publisher": {"@type": "Organization", "name": provider_name},
                "applicationCategory": "GameApplication",
                "genre": "Slot Online",
                "operatingSystem": "WebBrowser",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(round(random.uniform(4.5, 4.9), 1)), "bestRating": "5", "ratingCount": str(random.randint(100, 5000))}
            }
            schema_json_str = json.dumps(schema_data, indent=4)

            # --- D. INJECT VARIABLES INTO TEMPLATE ---
            html_play = TEMPLATE_PLAY \
                .replace('{{ANALYTICS}}', analytics_code) \
                .replace('{{GAME_NAME}}', game['name']) \
                .replace('{{GAME_DESC}}', game['desc']) \
                .replace('{{RTP}}', game['rtp']) \
                .replace('{{VOLATILITY}}', game['volatility']) \
                .replace('{{PROVIDER}}', provider_name) \
                .replace('{{IFRAME_URL}}', iframe_url) \
                .replace('{{SITE_TITLE}}', target['site_title']) \
                .replace('{{CANONICAL_URL}}', canonical_url) \
                .replace('{{BACKLINK_URL}}', target['backlink_url']) \
                .replace('{{ACCENT_COLOR}}', target['accent_color']) \
                .replace('{{SCHEMA_JSON}}', schema_json_str) \
                .replace('{{BG_IMAGE_URL}}', proxy_bg_url) \
                .replace('{{POSTER_URL}}', proxy_poster_url) \
                .replace('{{RELATED_GAMES}}', related_html)

            # --- E. SAVE STATIC FILE ---
            with open(output_path, 'w', encoding='utf-8') as f: 
                f.write(html_play)
                generated_count += 1
            
            # --- F. PING SEARCH ENGINES ---
            ping_new_content(game['name'], page_url)
                
        print(f"   ✅ Finished. New files generated: {generated_count} in {game_dir}")
        
        # --- G. GENERATE SEO FILES ---
        generate_sitemap(root_path, domain_url, "game")
        generate_master_sitemap(root_path, domain_url)
        generate_robots_txt(root_path, domain_url)

    print(f"\n🎉 All tasks completed in {round(time.time() - start_time, 2)} seconds.")

if __name__ == "__main__":
    generate_play_pages()