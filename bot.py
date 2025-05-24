import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
import io
import random
import asyncio
import time
import re
import subprocess
import sys
import math
import traceback
from keep_alive import keep_alive
from datetime import datetime, timedelta  # Tu as déjà la bonne importation pour datetime et timedelta
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord import Interaction
import logging
from typing import Optional

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461
# Définir GUILD_ID
GUILD_ID = 1034007767050104892

# --- ID Etherya Partenariats ---
partnership_channel_id = 1355158081855688745
ROLE_ID = 1355157749994098860

# --- ID Etherya ---
BOUNTY_CHANNEL_ID = 1355298449829920950
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854

# --- ID Etherya Pouvoir ---
# -- Oeil Démoniaque --
OEIL_ID = 1363949082653098094
ROLE_ID = 1364123507532890182
# -- Float --
FLOAT_ID = 1363946902730575953
ROLE_FLOAT_ID = 1364121382908067890
# -- Pokeball --
POKEBALL_ID = 1363942048075481379
# -- Infini --
INFINI_ID = [1363939565336920084, 1363939567627145660, 1363939486844850388]
ANTI_ROB_ROLE = 1363964754678513664
# -- Armure du Berserker --
ARMURE_ID = 1363821649002238142
ANTI_ROB_ID = 1363964754678513664
# -- Rage du Berserker --
RAGE_ID = 1363821333624127618
ECLIPSE_ROLE_ID = 1364115033197510656
# -- Ultra Instinct --
ULTRA_ID = 1363821033060307106
# -- Haki des Rois --
HAKI_ROI_ID = 1363817645249527879
HAKI_SUBIS_ID = 1364109450197078026
# -- Arme Démoniaque Impérial --
ARME_DEMONIAQUE_ID = 1363817586466361514
# -- Heal (Appel de l'exorciste) --
HEAL_ID = 1363873859912335400
MALUS_ROLE_ID = 1363969965572755537
# -- Benediction --
BENEDICTION_ROLE_ID = 1364294230343684137
# -- Divin --
DIVIN_ROLE_ID = 1367567412886765589
# -- Bombe --
BOMBE_ID = 1365316070172393572
# -- Marine & Pirates --
ISEY_MARINE_ID = 1365631932964012142
ISEY_PIRATE_ID = 1365682636957421741

# --- ID Etherya Nen ---
# Rôle autorisé à utiliser le Nen
PERMISSION_ROLE_ID = 1363928528587984998
# ID de l'item requis
LICENSE_ITEM_ID = 7
# Roles par type de Nen
nen_roles = {
    "renforcement": 1363306813688381681,
    "emission": 1363817609916584057,
    "manipulation": 1363817536348749875,
    "materialisation": 1363817636793810966,
    "transformation": 1363817619529924740,
    "specialisation": 1363817593252876368,
}

# Chances de drop en %
nen_drop_rates = [
    ("renforcement", 24.5),
    ("emission", 24.5),
    ("manipulation", 16.5),
    ("materialisation", 16.5),
    ("transformation", 17.5),
    ("specialisation", 0.5),
]
# -- Materialisation --
MATERIALISATION_IDS = [1363817636793810966, 1363817593252876368]
# IDs d'items interdits à la matérialisation
ITEMS_INTERDITS = [202, 197, 425, 736, 872, 964, 987]
# -- Manipulation --
MANIPULATION_ROLE_ID = 1363974710739861676
AUTHORIZED_MANI_IDS = [1363817593252876368, 1363817536348749875]
# -- Emission --
EMISSION_IDS = [1363817593252876368, 1363817609916584057]
TARGET_ROLE_ID = 1363969965572755537 
# -- Renforcement --
RENFORCEMENT_IDS = [1363306813688381681, 1363817593252876368]
RENFORCEMENT_ROLE_ID = 1363306813688381681 

# --- ID Etherya Fruits du Démon ---
ROLE_UTILISATEUR_GLACE = 1365311608259346462
ROLE_GEL = 1365313259280007168

# --- ID Etherya Pirates & Marines ---
# Roles
marine_roles = {
    "Amiral en chef": 1365683477868970204,
    "Commandant": 1365683407023243304,
    "Lieutenant": 1365683324831531049,
    "Matelot": 1365683175019516054,
}

pirate_roles = {
    "Roi des Pirates": 1365682989996052520,
    "Yonko": 1365682989996052520,
    "Corsaire": 1365682918243958826,
    "Pirate": 1365682795501977610,
}

log_channels = {
    "sanctions": 1365674258591912018,
    "messages": 1365674387700977684,
    "utilisateurs": 1365674425394921602,
    "nicknames": 1365674498791051394,
    "roles": 1365674530793586758,
    "vocal": 1365674563458826271,
    "serveur": 1365674597692997662,
    "permissions": 1365674740915765278,
    "channels": 1365674773107052644,
    "webhooks": 1365674805143146506,
    "bots": 1365674841344049162,
    "boosts": 1365674914740441158
}

def get_log_channel(guild, key):
    log_channel_id = log_channels.get(key)
    if log_channel_id:
        return guild.get_channel(log_channel_id)
    return None

# Fonction pour créer des embeds formatés
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

# Connexion MongoDB
mongo_uri = os.getenv("MONGO_DB")  # URI de connexion à MongoDB
print("Mongo URI :", mongo_uri)  # Cela affichera l'URI de connexion (assure-toi de ne pas laisser cela en prod)
client = MongoClient(mongo_uri)
db = client['Cass-Eco2']

# Collections
collection = db['ether_eco']  #Stock les Bal
collection2 = db['ether_daily']  #Stock les cd de daily
collection3 = db['ether_slut']  #Stock les cd de slut
collection4 = db['ether_crime']  #Stock les cd de slut
collection5 = db['ether_collect'] #Stock les cd de collect
collection6 = db['ether_work'] #Stock les cd de Work
collection7 = db['ether_inventory'] #Stock les inventaires
collection8 = db['info_cf'] #Stock les Info du cf
collection9 = db['info_logs'] #Stock le Salon logs
collection10 = db['info_bj'] #Stock les Info du Bj
collection11 = db['info_rr'] #Stock les Info de RR
collection12 = db['info_roulette'] #Stock les Info de SM
collection13 = db['info_sm'] #Stock les Info de SM
collection14 = db['ether_rob'] #Stock les cd de Rob
collection15 = db['anti_rob'] #Stock les rôle anti-rob
collection16 = db['ether_boutique'] #Stock les Items dans la boutique
collection17 = db['joueur_ether_inventaire'] #Stock les items de joueurs
collection18 = db['ether_effects'] #Stock les effets
collection19 = db['ether_badge'] #Stock les bagde
collection20 = db['inventaire_badge'] #Stock les bagde des joueurs
collection21 = db['daily_badge'] #Stock les cd des daily badge
collection22 = db['start_date'] #Stock la date de commencemant des rewards
collection23 = db['joueur_rewards'] #Stock ou les joueurs sont
collection24 = db['cd_renforcement'] #Stock les cd
collection25 = db['cd_emission'] #Stock les cd
collection26 = db['cd_manipulation'] #Stock les cd
collection27 = db['cd_materialisation'] #Stock les cd
collection28 = db['cd_transformation'] #Stock les cd
collection29 = db['cd_specialisation'] #Stock les cd
collection30 = db['cd_haki_attaque'] #Stock les cd
collection31 = db['cd_haki_subis'] #Stock les cd
collection32 = db['ether_quetes'] #Stock les quetes
collection33 = db['inventory_collect'] #Stock les items de quetes
collection34 = db['collect_items'] #Stock les items collector
collection35 = db['ether_guild'] #Stock les Guild
collection36 = db['guild_inventaire'] #Stock les inventaire de Guild
collection37 = db['ether_bounty'] #Stock les Primes de Pirates
collection38 = db['ether_honor'] #Stock les Honor des Marines
collection39 = db['cd_capture_ether'] #Stock les cd d'attaque
collection40 = db['cd_bombe'] #Stock les cd des bombes
collection41 = db['cd_gura'] #Stock les cd de seismes
collection42 = db['cd_glace'] #Stock les cd d'attaque de glace
collection43 = db['glace_subis'] #Stock le cd avant de retirer le rôle de subis de glace
collection44 = db['cd_tenebre'] #Stock les cd de Yami
collection45 = db['cd_protection_tenebre'] #Stock le temps de protection de Yami
collection46 = db['cd_gear_second'] #Stock le cd des Gear Second
collection47 = db['cd_gear_fourth'] #Stock les cd des Gear Fourth
collection48 = db['cd_use_fourth'] #Stock les cd des utilisation du Gear Fourth
collection49 = db['cd_royaume_nika'] #Stock le cd des utilisation du Royaume
collection50 = db['cd_acces_royaume'] #Stock le cd d'acces au Royaume
collection51 = db['cd_nika_collect'] #Stock le cd de reutilisation du Nika Collect
collection52 = db['cd_eveil_attaque'] #Stock le cd de reutilisation du Nika Eveil
collection53 = db['cd_eveil_subis'] #Stock le cd de soumission du Nika Eveil
collection54 = db['cd_bourrasque'] #Stock le cd de reutilisation du Uo Uo no Mi
collection55 = db['cd_bourrasque_subis'] #Stock le cd de soumission du Uo Uo no Mi
collection56 = db['cd_tonnerre_attaque'] #Stock les cd de reutillisation du Tonnerre Divin
collection57 = db['cd_tonnerre_subis'] #Stock les cd de soumission du Tonnerre Divin
collection58 = db['cd_eveil_uo'] #Stock les cd d'eveil du Dragon
collection59 = db['message_jour'] #Stock les message des membres chaque jour
collection60 = db['cd_wobservation'] #Stock les cd de W Observation
collection61 = db['cd_observation']

# Fonction pour vérifier si l'utilisateur possède un item (fictif, à adapter à ta DB)
async def check_user_has_item(user: discord.Member, item_id: int):
    # Ici tu devras interroger la base de données MongoDB ou autre pour savoir si l'utilisateur possède cet item
    # Par exemple:
    # result = collection.find_one({"user_id": user.id, "item_id": item_id})
    # return result is not None
    return True  # Pour l'exemple, on suppose que l'utilisateur a toujours l'item.

def get_cf_config(guild_id):
    config = collection8.find_one({"guild_id": guild_id})
    if not config:
        # Valeurs par défaut
        config = {
            "guild_id": guild_id,
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        collection8.insert_one(config)
    return config

async def initialize_bounty_or_honor(user_id, is_pirate, is_marine):
    # Vérifier si le joueur est un pirate et n'a pas encore de prime
    if is_pirate:
        bounty_data = collection37.find_one({"user_id": user_id})
        if not bounty_data:
            # Si le joueur n'a pas de prime, initialiser à 50
            collection37.insert_one({"user_id": user_id, "bounty": 50})

    # Vérifier si le joueur est un marine et n'a pas encore d'honneur
    if is_marine:
        honor_data = collection38.find_one({"user_id": user_id})
        if not honor_data:
            # Si le joueur n'a pas d'honneur, initialiser à 50
            collection38.insert_one({"user_id": user_id, "honor": 50})

async def log_eco_channel(bot, guild_id, user, action, amount, balance_before, balance_after, note=""):
    config = collection9.find_one({"guild_id": guild_id})
    channel_id = config.get("eco_log_channel") if config else None

    if not channel_id:
        return  # Aucun salon configuré

    channel = bot.get_channel(channel_id)
    if not channel:
        return  # Salon introuvable (peut avoir été supprimé)

    embed = discord.Embed(
        title="💸 Log Économique",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else None)
    embed.add_field(name="Action", value=action, inline=True)
    embed.add_field(name="Montant", value=f"{amount} <:ecoEther:1341862366249357374>", inline=True)
    embed.add_field(name="Solde", value=f"Avant: {balance_before}\nAprès: {balance_after}", inline=False)

    if note:
        embed.add_field(name="Note", value=note, inline=False)

    await channel.send(embed=embed)

def load_guild_settings(guild_id):
    # Charger les données de la collection principale
    ether_eco_data = collection.find_one({"guild_id": guild_id}) or {}
    ether_daily_data = collection2.find_one({"guild_id": guild_id}) or {}
    ether_slut_data = collection3.find_one({"guild_id": guild_id}) or {}
    ether_crime_data = collection4.find_one({"guild_id": guild_id}) or {}
    ether_collect = collection5.find_one({"guild_id": guild_id}) or {}
    ether_work_data = collection6.find_one({"guild_id": guild_id}) or {}
    ether_inventory_data = collection7.find_one({"guild_id": guild_id}) or {}
    info_cf_data = collection8.find_one({"guild_id": guild_id}) or {}
    info_logs_data = collection9.find_one({"guild_id": guild_id}) or {}
    info_bj_data = collection10.find_one({"guild_id": guild_id}) or {}
    info_rr_data = collection11.find_one({"guild_id": guild_id}) or {}
    info_roulette_data = collection12.find_one({"guild_id": guild_id}) or {}
    info_sm_roulette_data = collection13.find_one({"guild_id": guild_id}) or {}
    ether_rob_data = collection14.find_one({"guild_id": guild_id}) or {}
    anti_rob_data = collection15.find_one({"guild_id": guild_id}) or {}
    ether_boutique_data = collection16.find_one({"guild_id": guild_id}) or {}
    joueur_ether_inventaire_data = collection17.find_one({"guild_id": guild_id}) or {}
    ether_effects_data = collection18.find_one({"guild_id": guild_id}) or {}
    ether_badge_data = collection19.find_one({"guild_id": guild_id}) or {}
    inventaire_badge_data = collection20.find_one({"guild_id": guild_id}) or {}
    daily_badge_data = collection21.find_one({"guild_id": guild_id}) or {}
    start_date_data = collection22.find_one({"guild_id": guild_id}) or {}
    joueur_rewards_data = collection23.find_one({"guild_id": guild_id}) or {}
    cd_renforcement_data = collection24.find_one({"guild_id": guild_id}) or {}
    cd_emission_data = collection25.find_one({"guild_id": guild_id}) or {}
    cd_manipultation_data = collection26.find_one({"guild_id": guild_id}) or {}
    cd_materialisation_data = collection27.find_one({"guidl_id": guild_id}) or {}
    cd_transformation_data = collection28.find_one({"guild_id": guild_id}) or {}
    cd_specialisation_data = collection29.find_one({"guild_id": guild_id}) or {}
    cd_haki_attaque_data = collection30.find_one({"guild_id": guild_id}) or {}
    cd_haki_subis_data = collection31.find_one({"guild_id": guild_id}) or {}
    ether_quetes_data = collection32.find_one({"guild_id": guild_id}) or {}
    inventory_collect_data = collection33.find_one({"guild_id": guild_id}) or {}
    collect_items_data = collection34.find_one({"guild_id": guild_id}) or {}
    ether_guild_data = collection35.find_one({"guild_id": guild_id}) or {}
    guild_inventaire_data = collection36.find_one({"guild_id": guild_id}) or {}
    ether_bounty_data = collection37.find_one({"guild_id": guild_id}) or {}
    ether_honnor_data = collection38.find_one({"guild_id": guild_id}) or {}
    cd_capture_ether_data = collection39.find_one({"guild_id": guild_id}) or {}
    cd_bombe_data = collection40.find_one({"guild_id": guild_id}) or {}
    cd_gura_data = collection41.find_one({"guild_id": guild_id}) or {}
    cd_glace_data = collection42.fing_one({"guild_id": guild_id}) or {}
    glace_subis_data = collection43.find_one({"guild_id": guild_id}) or {}
    cd_tenebre_data = collection44.find_one({"guild_id": guild_id}) or {}
    cd_protection_tenebre_data = collection45.find_one({"guild_id": guild_id}) or {}
    cd_gear_second_data = collection46.find_one({"guild_id": guild_id}) or {}
    cd_gear_fourth_data = collection47.find_one({"guild_id": guild_id}) or {}
    cd_use_fourth_data = collection48.find_one({"guild_id": guild_id}) or {}
    cd_royaume_nika_data = collection49.find_one({"guild_id": guild_id}) or {}
    cd_acces_royaume_data = collection50.find_one({"guild_id": guild_id}) or {}
    cd_nika_collect_data = collection51.find_one({"guild_id": guild_id}) or {}
    cd_eveil_attaque_data = collection52.find_one({"guild_id": guild_id}) or {}
    cd_eveil_subis_data = collection53.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_data = collection54.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_subis_data = collection55.find_one({"guild_id": guild_id}) or {}
    cd_tonnerre_attaque_data = collection56.find_one({"guild_id": guil_id}) or {}
    cd_tonnerre_subis_data = collection57.find_one({"guild_id": guild_id}) or {}
    cd_eveil_uo_data = collection58.find_one({"guild_id": guild_id}) or {}
    message_jour_data = collection59.find_one({"guild_id": guild_id}) or {}
    cd_wobservation_data = collection60.find_one({"guild_id": guild_id}) or {}
    cd_observation_data = collection61.find_one({"guild_id": guild_id}) or {}
    
    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
        "ether_eco": ether_eco_data,
        "ether_daily": ether_daily_data,
        "ether_slut": ether_slut_data,
        "ether_crime": ether_crime_data,
        "ether_collect": ether_collect_data,
        "ether_work": ether_work_data,
        "ether_inventory": ether_inventory_data,
        "info_cf": info_cf_data,
        "info_logs": info_logs_data,
        "info_bj": info_bj_data,
        "info_rr": info_rr_data,
        "info_roulette": info_roulette_data,
        "info_sm": info_sm_data,
        "ether_rob": ether_rob_data,
        "anti_rob": anti_rob_data,
        "ether_boutique": ether_boutique_data,
        "joueur_ether_inventaire": joueur_ether_inventaire_data,
        "ether_effects": ether_effects_data,
        "ether_badge": ether_badge_data,
        "inventaire_badge": inventaire_badge_data,
        "daily_badge": daily_badge_data,
        "start_date": start_date_data,
        "joueur_rewards": joueur_rewards_data,
        "cd_renforcement": cd_renforcement_data,
        "cd_emission": cd_emission_data,
        "cd_manipultation": cd_manipultation_data,
        "cd_materialisation": cd_materialisation_data,
        "cd_transformation" : cd_transformation_data,
        "cd_specialisation" : cd_specialisation_data,
        "cd_haki_attaque": cd_haki_attaque_data,
        "cd_haki_subis": cd_haki_subis_data,
        "ether_quetes": ether_quetes_data,
        "inventory_collect": inventory_collect_data,
        "collect_items": collect_items_data,
        "ether_guild": ether_guild_data,
        "guild_inventaire": guild_inventaire_data,
        "ether_bounty": ether_bounty_data,
        "ether_honnor": ether_honnor_data,
        "cd_capture_ether": cd_capture_ether_data,
        "cd_bombe": cd_bombe_data,
        "cd_gura": cd_gura_data,
        "cd_glace": cd_glace_data,
        "glace_subis": glace_subis_data,
        "cd_tenebre": cd_tenebre_data,
        "cd_protection_tenebre": cd_protection_tenebre_data,
        "cd_gear_second": cd_gear_second_data,
        "cd_gear_fourth": cd_gear_fourth_data,
        "cd_use_fourth": cd_use_fourth_data,
        "cd_royaume_nika": cd_royaume_nika_data,
        "cd_acces_royaume": cd_acces_royaume_data,
        "cd_nika_collect": cd_nika_collect_data,
        "cd_eveil_attaque": cd_eveil_attaque_data,
        "cd_eveil_subis": cd_eveil_subis_data,
        "cd_bourrasque": cd_bourrasque_data,
        "cd_bourrasque_subis": cd_bourrasque_subis_data,
        "cd_tonnerre_attaque": cd_tonnerre_attaque_data,
        "cd_tonnerre_subis": cd_tonnerre_subis_data,
        "cd_eveil_uo": cd_eveil_uo_data,
        "message_jour": message_jour_data,
        "cd_wobservation": cd_wobservation_data,
        "cd_observation": cd_observation_data
    }

    return combined_data

def get_or_create_user_data(guild_id: int, user_id: int):
    data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not data:
        data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection.insert_one(data)
    return data

# --- Boucle Auto Collect ---
import discord
from discord.ext import tasks
from datetime import datetime
import time


# --- Boucle suppression des rôles Bourrasque ---
@tasks.loop(minutes=10)
async def remove_bourrasque_roles():
    now = datetime.utcnow()
    expired = collection54.find({"end_time": {"$lte": now}})

    for doc in expired:
        guild = bot.get_guild(doc["guild_id"])
        member = guild.get_member(doc["user_id"])
        role = guild.get_role(doc["role_id"])

        if member and role:
            try:
                await member.remove_roles(role)
                print(f"✅ Rôle retiré de {member.display_name}")
            except Exception as e:
                print(f"❌ Erreur lors du retrait du rôle: {e}")

        # Supprime l'entrée après retrait
        collection54.delete_one({"_id": doc["_id"]})

# --- Boucle suppression des rôles de gel économique ---
@tasks.loop(minutes=30)
async def remove_glace_roles():
    now = datetime.utcnow()
    users_to_unfreeze = collection43.find({"remove_at": {"$lte": now}})
    role_id = 1365063792513515570

    for user_data in users_to_unfreeze:
        guild = bot.get_guild(VOTRE_GUILD_ID)  # Remplace par l'ID de ton serveur
        member = guild.get_member(user_data["user_id"])
        if member:
            role = guild.get_role(role_id)
            if role in member.roles:
                await member.remove_roles(role, reason="Fin du gel économique")
        collection43.delete_one({"user_id": user_data["user_id"]})

# --- Boucle réinitialisation des primes et honneurs ---
@tasks.loop(hours=168)
async def reset_bounties_and_honor():
    collection37.update_many({}, {"$set": {"bounty": 50}})
    collection38.update_many({}, {"$set": {"honor": 50}})
    await redistribute_roles()

async def redistribute_roles():
    # Logique pour réattribuer les rôles en fonction de la prime ou de l'honneur
    pass

# --- Initialisation au démarrage ---
@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté.")
    bot.loop.create_task(start_background_tasks())
    bot.uptime = time.time()
    activity = discord.Activity(
        type=discord.ActivityType.streaming,
        name="Etherya",
        url="https://discord.com/oauth2/authorize?client_id=1356693934012891176"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)

    print(f"🎉 **{bot.user}** est maintenant connecté et affiche son activité de stream avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

# --- Démarrer les tâches en arrière-plan ---
async def start_background_tasks():
    if not task_annonce_jour.is_running():
        task_annonce_jour.start()
    if not reset_bounties_and_honor.is_running():
        reset_bounties_and_honor.start()
    if not auto_collect_loop.is_running():
        auto_collect_loop.start()
    if not remove_glace_roles.is_running():
        remove_glace_roles.start()
    if not remove_bourrasque_roles.is_running():
        remove_bourrasque_roles.start()

# --- Gestion globale des erreurs ---
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    try:
        await args[0].response.send_message(embed=embed)
    except Exception:
        pass

@bot.hybrid_command(
    name="uptime",
    description="Affiche l'uptime du bot."
)
async def uptime(ctx):
    uptime_seconds = round(time.time() - start_time)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    embed = discord.Embed(
        title="Uptime du bot",
        description=f"Le bot est en ligne depuis : {days} jours, {hours} heures, {minutes} minutes, {seconds} secondes",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"♥️by Iseyg", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.hybrid_command(
    name="ping",
    description="Affiche le Ping du bot."
)
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Latence en ms
    embed = discord.Embed(title="Pong!", description=f"Latence: {latency}ms", color=discord.Color.green())

    await ctx.send(embed=embed)

# Vérification si l'utilisateur est l'owner du bot
def is_owner(ctx):
    return ctx.author.id == ISEY_ID

@bot.command()
async def restart(ctx):
    if is_owner(ctx):
        embed = discord.Embed(
            title="Redémarrage du Bot",
            description="Le bot va redémarrer maintenant...",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)  # Redémarre le bot
    else:
        await ctx.send("Seul l'owner peut redémarrer le bot.")

@bot.hybrid_command()
async def shutdown(ctx):
    if is_owner(ctx):
        embed = discord.Embed(
            title="Arrêt du Bot",
            description="Le bot va maintenant se fermer. Tous les services seront arrêtés.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Cette action est irréversible.")
        await ctx.send(embed=embed)
        await bot.close()
    else:
        await ctx.send("Seul l'owner peut arrêter le bot.")

#------------------------------------------------------------------------- Nen
# === Vérifie si le joueur a une licence Hunter (item 7)
def has_license(user_id, guild_id):
    items_cursor = collection17.find({"guild_id": guild_id, "user_id": user_id})
    for item in items_cursor:
        if item["item_id"] == LICENSE_ITEM_ID:
            return True
    return False

# === Sélection aléatoire du Nen selon les chances
def get_random_nen():
    roll = random.uniform(0, 100)
    total = 0
    for nen_type, chance in nen_drop_rates:
        total += chance
        if roll <= total:
            return nen_type
    return "renforcement"  # fallback (improbable)

# === Commande Nen (ROLL)
@bot.command()
async def nen(ctx):
    user = ctx.author
    guild = ctx.guild

    # Vérif rôle autorisé
    permission_role = discord.utils.get(guild.roles, id=PERMISSION_ROLE_ID)
    if permission_role not in user.roles:
        return await ctx.send("❌ Tu n'es pas digne d'utiliser le Nen.")

    # Vérif licence Hunter
    if not has_license(user.id, guild.id):
        return await ctx.send("❌ Tu n'as pas de Licence Hunter (item ID 7) dans ton inventaire.")

    # Sélection Nen
    nen_type = get_random_nen()
    role_id = nen_roles.get(nen_type)
    nen_role = discord.utils.get(guild.roles, id=role_id)

    # Attribution du rôle Nen
    if nen_role:
        try:
            await user.add_roles(nen_role)
        except discord.Forbidden:
            return await ctx.send("⚠️ Je n’ai pas la permission d’attribuer des rôles.")

    # Embed de résultat
    color = discord.Color.blue()
    if nen_type == "specialisation":
        color = discord.Color.purple()

    embed = discord.Embed(
        title="🎴 Résultat du Nen Roll",
        description=f"Tu as éveillé le Nen de type **{nen_type.capitalize()}** !",
        color=color
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    embed.set_footer(text="Utilise tes pouvoirs avec sagesse... ou pas.")

    await ctx.send(embed=embed)

#-------------------------------------- Renforcement

COOLDOWN_DAYS = 7
DURATION_HOURS = 24

@bot.command(name="renforcement")
async def renforcement(ctx):
    user = ctx.author
    guild = ctx.guild
    now = datetime.utcnow()

    # Vérifie que l'utilisateur a un des rôles autorisés
    if not any(role.id in RENFORCEMENT_IDS for role in user.roles):
        return await ctx.send("❌ Tu n'as pas le rôle requis pour utiliser cette commande.")

    # Vérifie le cooldown dans MongoDB
    cd_data = collection24.find_one({"user_id": user.id})
    if cd_data and "last_used" in cd_data:
        last_used = cd_data["last_used"]
        if now - last_used < timedelta(days=COOLDOWN_DAYS):
            remaining = (last_used + timedelta(days=COOLDOWN_DAYS)) - now
            hours, minutes = divmod(remaining.total_seconds() // 60, 60)
            return await ctx.send(f"⏳ Tu dois encore attendre {int(hours)}h{int(minutes)} avant de pouvoir réutiliser cette commande.")

    # Donne le rôle temporairement
    role = guild.get_role(RENFORCEMENT_ROLE_ID)
    if not role:
        return await ctx.send("❌ Le rôle de renforcement n'existe pas.")

    await user.add_roles(role, reason="Renforcement activé")

    # Embed joli avec image
    embed = discord.Embed(
        title="💪 Renforcement Activé",
        description=f"Tu as reçu le rôle **{role.name}** pour 24h.",
        color=discord.Color.green(),
        timestamp=now
    )
    embed.set_footer(text="Cooldown de 7 jours")
    embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else None)
    embed.set_image(url="https://github.com/Iseyg91/Isey_aime_Cass/blob/main/IMAGE%20EMBED%20NEN/renfo.jpg?raw=true")  # Ajoute l'image

    await ctx.send(embed=embed)

    # Met à jour le cooldown dans Mongo
    collection24.update_one(
        {"user_id": user.id},
        {"$set": {"last_used": now}},
        upsert=True
    )

    # Attendre 24h puis retirer le rôle
    await asyncio.sleep(DURATION_HOURS * 3600)
    if role in user.roles:
        try:
            await user.remove_roles(role, reason="Renforcement expiré")
            try:
                await user.send("⏳ Ton rôle **Renforcement** a expiré après 24h.")
            except discord.Forbidden:
                pass
        except discord.HTTPException:
            pass

#-------------------------------------- Emission

COOLDOWN_DAYS = 1 

@bot.command(name="emission")
async def emission(ctx, member: discord.Member):
    # Vérification du rôle
    if not any(role.id in EMISSION_IDS for role in ctx.author.roles):
        return await ctx.send("❌ Tu n'as pas le Nen nécessaire pour utiliser cette technique.")

    # Cooldown MongoDB
    cooldown = collection25.find_one({"user_id": ctx.author.id})
    now = datetime.utcnow()
    if cooldown and now < cooldown["next_use"]:
        remaining = cooldown["next_use"] - now
        return await ctx.send(f"⏳ Tu dois attendre encore {remaining.days}j {remaining.seconds // 3600}h.")

    # Appliquer le rôle malus
    role = ctx.guild.get_role(TARGET_ROLE_ID)
    await member.add_roles(role)

    # Enregistrer cooldown
    collection25.update_one(
        {"user_id": ctx.author.id},
        {"$set": {"next_use": now + timedelta(days=COOLDOWN_DAYS)}},
        upsert=True
    )

    # Embed stylé avec image
    embed = discord.Embed(
        title="🌑 Emission : Technique Maudite",
        description=f"{member.mention} a été maudit pendant 24h.\nIl subira un malus de **-20%** sur ses collect !",
        color=discord.Color.dark_purple(),
        timestamp=now
    )
    embed.set_footer(text="Utilisation du Nen : Emission")
    embed.set_image(url="https://github.com/Iseyg91/Isey_aime_Cass/blob/main/IMAGE%20EMBED%20NEN/emission.jpg?raw=true")  # Ajout de l'image

    await ctx.send(embed=embed)

    # Attendre 24h et retirer le rôle
    await asyncio.sleep(86400)  # 24h en secondes
    await member.remove_roles(role)

#------------------------------------- Manipulation

COOLDOWN_DAYS = 7

@bot.command(name='manipulation')
@commands.guild_only()
async def manipulation(ctx):
    user = ctx.author
    guild = ctx.guild

    # Vérifie si l'utilisateur a l'un des rôles autorisés
    if not any(role.id in AUTHORIZED_MANI_IDS for role in user.roles):
        return await ctx.send("⛔ Tu n'as pas accès à cette commande.")

    # Vérifie le cooldown en DB
    cooldown_data = collection26.find_one({"user_id": user.id})
    now = datetime.utcnow()

    if cooldown_data and now < cooldown_data["next_available"]:
        remaining = cooldown_data["next_available"] - now
        hours, remainder = divmod(remaining.total_seconds(), 3600)
        minutes = remainder // 60
        return await ctx.send(f"⏳ Tu dois attendre encore {int(hours)}h{int(minutes)}m avant de réutiliser cette commande.")

    # Donne le rôle de manipulation
    role = guild.get_role(MANIPULATION_ROLE_ID)
    if not role:
        return await ctx.send("❌ Le rôle de manipulation est introuvable.")

    await user.add_roles(role)

    # Embed avec image
    embed = discord.Embed(
        title="🧠 Manipulation Activée",
        description="Tu gagnes un **collect de 1%** toutes les 4h pendant 24h.",
        color=discord.Color.blue(),
        timestamp=now
    )
    embed.set_footer(text="Cooldown de 7 jours")
    embed.set_image(url="https://github.com/Iseyg91/Isey_aime_Cass/blob/main/IMAGE%20EMBED%20NEN/image0.jpg?raw=true")  # Ajout de l'image

    await ctx.send(embed=embed)

    # Mets à jour le cooldown
    next_available = now + timedelta(days=COOLDOWN_DAYS)
    collection26.update_one(
        {"user_id": user.id},
        {"$set": {"next_available": next_available}},
        upsert=True
    )

    # Supprime le rôle après 24h
    await asyncio.sleep(86400)
    await user.remove_roles(role)
    try:
        await user.send("💤 Ton effet **Manipulation** est terminé.")
    except discord.Forbidden:
        pass

#----------------------------------------- Materialisation
# Cooldown en heures
MATERIALISATION_COOLDOWN_HOURS = 6

@bot.command(name="materialisation")
async def materialisation(ctx):
    user_id = ctx.author.id
    guild_id = ctx.guild.id
    now = datetime.utcnow()

    # Vérifie le cooldown
    cd_doc = collection27.find_one({"user_id": user_id, "guild_id": guild_id})
    if cd_doc:
        last_use = cd_doc.get("last_use")
        if last_use and now < last_use + timedelta(hours=MATERIALISATION_COOLDOWN_HOURS):
            remaining = (last_use + timedelta(hours=MATERIALISATION_COOLDOWN_HOURS)) - now
            hours, remainder = divmod(remaining.total_seconds(), 3600)
            minutes = remainder // 60
            embed = discord.Embed(
                title="⏳ Cooldown actif",
                description=f"Tu dois encore attendre **{int(hours)}h {int(minutes)}m** avant de matérialiser un item.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)

    # Récupère un item aléatoire de la boutique (en stock uniquement, et pas interdit)
    items = list(collection16.find({
        "quantity": {"$gt": 0},
        "id": {"$in": MATERIALISATION_IDS, "$nin": ITEMS_INTERDITS}
    }))
    
    if not items:
        embed = discord.Embed(
            title="❌ Aucun item disponible",
            description="Il n'y a pas d'items à matérialiser actuellement.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    selected_item = random.choice(items)

    # Met à jour l'inventaire simple
    existing = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
    if existing:
        inventory = existing.get("items", {})
        inventory[str(selected_item["id"])] = inventory.get(str(selected_item["id"]), 0) + 1
        collection7.update_one(
            {"user_id": user_id, "guild_id": guild_id},
            {"$set": {"items": inventory}}
        )
    else:
        collection7.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "items": {str(selected_item["id"]): 1}
        })

    # Ajoute à l'inventaire structuré
    collection17.insert_one({
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": selected_item["id"],
        "item_name": selected_item["title"],
        "emoji": selected_item.get("emoji"),
        "price": selected_item["price"],
        "obtained_at": now
    })

    # Met à jour le cooldown
    collection27.update_one(
        {"user_id": user_id, "guild_id": guild_id},
        {"$set": {"last_use": now}},
        upsert=True
    )

    # Message de confirmation avec image
    embed = discord.Embed(
        title="✨ Matérialisation réussie",
        description=f"Tu as matérialisé **{selected_item['emoji']} {selected_item['title']}** !",
        color=discord.Color.green()
    )
    embed.set_image(url="https://github.com/Iseyg91/Isey_aime_Cass/blob/main/IMAGE%20EMBED%20NEN/Materi.png?raw=true")
    await ctx.send(embed=embed)
    
#------------------------------------------ Transformation

@bot.command(
    name="transformation",
    description="Transforme ton aura en éclair et foudroie la banque d'un autre joueur pour lui retirer 25% de son solde bancaire.",
)
async def transformation(ctx: commands.Context, target: discord.User):
    # Vérifier si l'utilisateur a un des rôles autorisés
    if not any(role.id in [1363817593252876368, 1363817619529924740] for role in ctx.author.roles):
        return await ctx.send("Désolé, tu n'as pas le rôle nécessaire pour utiliser cette commande.")

    # Vérifier si l'utilisateur cible est valide
    if target == ctx.author:
        return await ctx.send("Tu ne peux pas utiliser cette commande sur toi-même.")

    guild_id = ctx.guild.id
    user_id = ctx.author.id
    target_id = target.id

    # Vérifier le cooldown
    cooldown_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if cooldown_data:
        last_used = cooldown_data.get("last_used")
        if last_used and (datetime.utcnow() - last_used).days < 14:
            remaining_days = 14 - (datetime.utcnow() - last_used).days
            return await ctx.send(f"Tu as déjà utilisé cette commande récemment. Essaie dans {remaining_days} jours.")

    # Récupérer les données de la banque de la cible
    target_data = collection.find_one({"guild_id": guild_id, "user_id": target_id})
    if not target_data:
        target_data = {"guild_id": guild_id, "user_id": target_id, "cash": 0, "bank": 0}
        collection.insert_one(target_data)

    # Calculer la perte de la banque de la cible (25%)
    bank_loss = target_data.get("bank", 0) * 0.25
    new_bank_balance = target_data["bank"] - bank_loss

    # Mettre à jour la banque de la cible
    collection.update_one({"guild_id": guild_id, "user_id": target_id}, {"$set": {"bank": new_bank_balance}})

    # Enregistrer le temps de la dernière utilisation pour le cooldown
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_used": datetime.utcnow()}},
        upsert=True,
    )

    # Log de l'action
    await log_eco_channel(
        bot=ctx.bot,
        guild_id=guild_id,
        user=ctx.author,
        action="Foudroie la banque de",
        amount=bank_loss,
        balance_before=target_data["bank"],
        balance_after=new_bank_balance,
        note=f"Transformation de l'aura en éclair. Perte de 25% de la banque de {target.display_name}."
    )

    # Embed stylé avec image
    embed = discord.Embed(
        title="⚡ Transformation : Aura en Éclair",
        description=f"Tu as transformé ton aura en éclair et foudroyé la banque de {target.display_name}, lui retirant {bank_loss:.2f} d'Ether.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Utilisation du Nen : Transformation")
    embed.set_image(url="https://github.com/Iseyg91/Isey_aime_Cass/blob/main/IMAGE%20EMBED%20NEN/Transfo.jpg?raw=true")  # Ajout de l'image

    await ctx.send(embed=embed)

#-------------------------------------------- Heal
# Commande .heal
@bot.command()
async def heal(ctx):
    # Vérifier si l'utilisateur a le rôle requis
    if HEAL_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("Désolé, vous n'avez pas l'autorisation de retirer ce Nen.")
        return

    # Retirer le rôle malus à la personne
    malus_role = discord.utils.get(ctx.guild.roles, id=MALUS_ROLE_ID)
    if malus_role in ctx.author.roles:
        await ctx.author.remove_roles(malus_role)
        await ctx.send(f"Le rôle malus a été retiré à {ctx.author.mention}.")

    # Retirer le rôle de soin (HEAL_ID)
    heal_role = discord.utils.get(ctx.guild.roles, id=HEAL_ID)
    if heal_role in ctx.author.roles:
        await ctx.author.remove_roles(heal_role)
        await ctx.send(f"Le rôle de soin a été retiré à {ctx.author.mention}.")

    # Créer l'embed avec l'image spécifiée
    embed = discord.Embed(title="Soin Exorciste", description="Le Nen a été retiré grâce à l'exorciste.", color=discord.Color.green())
    embed.set_image(url="https://preview.redd.it/q1xtzkr219371.jpg?width=1080&crop=smart&auto=webp&s=ce05b77fe67949cc8f6c39c01a9dd93c77af1fe8")

    # Envoyer l'embed
    await ctx.send(embed=embed)

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#----------------------------------------------- Imperial

@bot.command(name="imperial")
async def imperial(ctx, cible: discord.Member = None):
    auteur = ctx.author

    # Vérification si la cible est précisée
    if not cible:
        logger.warning(f"{auteur} a tenté d'utiliser la commande 'imperial' sans spécifier de cible.")
        return await ctx.send("❌ Tu dois spécifier une cible pour utiliser cette commande.")

    # Vérifie que l'utilisateur a le rôle spécial
    if ARME_DEMONIAQUE_ID not in [r.id for r in auteur.roles]:
        return await ctx.send("❌ Tu n'as pas le pouvoir démoniaque pour utiliser cette commande.")

    # Vérifie que la cible n'est pas un bot
    if cible.bot:
        return await ctx.send("❌ Tu ne peux pas cibler un bot.")

    # Vérifie que l'utilisateur ne cible pas lui-même
    if auteur.id == cible.id:
        return await ctx.send("❌ Tu ne peux pas te voler toi-même.")

    guild_id = ctx.guild.id

    def get_or_create_user_data(user_id):
        data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
        if not data:
            logger.info(f"Création de données pour l'utilisateur {user_id}")
            data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
            collection.insert_one(data)
        return data

    data_auteur = get_or_create_user_data(auteur.id)
    data_cible = get_or_create_user_data(cible.id)

    if "cash" not in data_cible or "bank" not in data_cible:
        logger.warning(f"Les données de {cible.id} sont corrompues. Création de nouvelles données.")
        data_cible["cash"] = 1500
        data_cible["bank"] = 0
        collection.update_one(
            {"guild_id": guild_id, "user_id": cible.id},
            {"$set": {"cash": 1500, "bank": 0}}
        )

    try:
        total_auteur = data_auteur["cash"] + data_auteur["bank"]
        total_cible = data_cible["cash"] + data_cible["bank"]
    except KeyError as e:
        logger.error(f"Erreur d'accès aux données : {e}")
        return await ctx.send(f"❌ Une erreur est survenue lors de l'accès aux données de {cible.display_name}.")

    if total_cible <= total_auteur:
        return await ctx.send("❌ Tu ne peux voler que quelqu'un de plus riche que toi.")

    roll = random.randint(15, 75)
    pourcentage = roll / 100
    vol_total = int(total_cible * pourcentage)

    vol_cash = min(vol_total, data_cible["cash"])
    vol_bank = vol_total - vol_cash

    if vol_total > total_cible:
        return await ctx.send("❌ Il n'y a pas assez de fonds disponibles à voler.")

    collection.update_one(
        {"guild_id": guild_id, "user_id": cible.id},
        {"$inc": {"cash": -vol_cash, "bank": -vol_bank}}
    )
    collection.update_one(
        {"guild_id": guild_id, "user_id": auteur.id},
        {"$inc": {"cash": vol_total}}
    )

    role = ctx.guild.get_role(ARME_DEMONIAQUE_ID)
    if role is None:
        logger.error(f"Le rôle ARME_DEMONIAQUE_ID ({ARME_DEMONIAQUE_ID}) n'a pas été trouvé.")
        return await ctx.send("❌ Le rôle d'arme démoniaque n'existe pas.")
    
    await auteur.remove_roles(role)

    emoji_currency = "<:ecoEther:1341862366249357374>"
    embed = discord.Embed(
        title="Pouvoir Impérial Démoniaque Utilisé !",
        description=(
            f"**{auteur.mention}** a utilisé son arme démoniaque sur **{cible.mention}** !\n"
            f"🎲 Le démon a jugé ton vol à **{roll}%** !\n"
            f"💸 Tu lui as volé **{vol_total:,} {emoji_currency}** !"
        ),
        color=discord.Color.dark_red()
    )
    embed.set_image(url="https://pm1.aminoapps.com/6591/d1e3c1527dc792f004068d914ca00c411031ccd2_hq.jpg")
    
    await ctx.send(embed=embed)

async def is_on_cooldown(user_id):
    print(f"[LOG] Recherche du cooldown MongoDB pour {user_id}")
    cooldown = collection30.find_one({"user_id": user_id})
    if cooldown:
        last_used = cooldown["last_used"]
        print(f"[LOG] Dernière utilisation trouvée : {last_used} ({type(last_used)})")
        cooldown_time = timedelta(weeks=2)
        if datetime.utcnow() - last_used < cooldown_time:
            print("[LOG] Cooldown actif")
            return True
        else:
            print("[LOG] Cooldown expiré")
    else:
        print("[LOG] Aucun cooldown trouvé pour cet utilisateur")
    return False

async def apply_haki_role(ctx, user):
    try:
        print("[LOG] Début de apply_haki_role")

        print(f"[LOG] Vérification du cooldown pour l'utilisateur : {user.id}")
        if await is_on_cooldown(user.id):
            print("[LOG] Utilisateur encore en cooldown")
            await ctx.send(f"{user.mention} doit attendre 2 semaines avant d'être ciblé à nouveau.")
            return
        print("[LOG] Utilisateur pas en cooldown")

        role = discord.utils.get(ctx.guild.roles, id=HAKI_SUBIS_ID)
        if not role:
            print("[ERREUR] Rôle Haki non trouvé dans le serveur")
            await ctx.send("Erreur : le rôle Haki à attribuer n'a pas été trouvé.")
            return
        print(f"[LOG] Rôle trouvé : {role.name}")

        await user.add_roles(role)
        print(f"[LOG] Rôle ajouté à {user.name}")
        await ctx.send(f"{user.mention} a été paralysé avec le Haki des Rois pour 7 jours.")

        now = datetime.utcnow()
        print(f"[LOG] Mise à jour du cooldown à {now}")
        collection30.update_one(
            {"user_id": user.id},
            {"$set": {"last_used": now}},
            upsert=True
        )
        print("[LOG] Cooldown enregistré en base de données")

        print("[LOG] Attente 7 jours (asyncio.sleep)")
        await asyncio.sleep(7 * 24 * 60 * 60)

        await user.remove_roles(role)
        print(f"[LOG] Rôle retiré de {user.name}")
        await ctx.send(f"{user.mention} est maintenant libéré du Haki des Rois.")

    except Exception as e:
        print(f"[ERREUR] Exception dans apply_haki_role : {type(e).__name__} - {e}")
        await ctx.send(f"Une erreur est survenue pendant l'application du Haki : `{type(e).__name__} - {e}`")

#-------------------------------------------- Haki des Rois
# Commande .haki
@bot.command()
@commands.has_role(HAKI_ROI_ID)
async def haki(ctx, user: discord.Member):
    """Applique le Haki des Rois à un utilisateur."""

    # Embed d'annonce
    embed = discord.Embed(
        title="⚡ Haki des Rois ⚡",
        description=f"{user.mention} a été frappé par le Haki des Rois !",
        color=discord.Color.purple(),
        timestamp=datetime.utcnow()
    )
    embed.set_image(url="https://static.wikia.nocookie.net/onepiece/images/4/42/Haoshoku_Haki_Choc.png/revision/latest?cb=20160221111336&path-prefix=fr")
    await ctx.send(embed=embed)

    # Application du Haki
    await apply_haki_role(ctx, user)

@haki.error
async def haki_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        print("[ERREUR] Permission manquante pour utiliser .haki")
        await ctx.send("Vous n'avez pas le rôle requis pour utiliser cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print("[ERREUR] Argument manquant : utilisateur")
        await ctx.send("Vous devez mentionner un utilisateur : `.haki @utilisateur`")
    else:
        print(f"[ERREUR] Erreur dans haki : {type(error).__name__} - {error}")
        await ctx.send("Une erreur est survenue lors de l'exécution de la commande.")

#----------------------------------------------------- Ultra Instinct
class MissingUltraRole(commands.CheckFailure):
    pass

@bot.command(name="ultra")
@commands.cooldown(1, 432000, commands.BucketType.user)  # 432000 sec = 5 jours
async def ultra(ctx):
    # Vérifie si l'utilisateur a le rôle ULTRA
    if not any(role.id == ULTRA_ID for role in ctx.author.roles):
        raise MissingUltraRole()

    embed = discord.Embed(
        title="☁️ Ultra Instinct ☁️",
        description=(
            "Vous utilisez la **forme ultime du Ultra Instinct**.\n"
            "Pendant un certain temps, vous **esquivez toutes les attaques** et devenez **totalement immunisé**.\n\n"
            "⚠️ Cette forme utilise énormément de votre ki...\n"
            "⏳ Il vous faudra **5 jours** de repos avant de pouvoir l'utiliser à nouveau."
        ),
        color=discord.Color.purple()
    )
    embed.set_image(url="https://dragonballsuper-france.fr/wp-content/uploads/2022/05/Dragon-Ball-Legends-Goku-Ultra-Instinct.jpg")
    embed.set_footer(text=f"Activé par {ctx.author.display_name}")

    await ctx.send(embed=embed)

@ultra.error
async def ultra_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = str(timedelta(seconds=int(error.retry_after)))
        await ctx.send(f"🕒 Vous devez attendre encore **{remaining}** avant de réutiliser cette forme ultime.")
    elif isinstance(error, MissingUltraRole):
        await ctx.send("❌ Vous n'avez pas la puissance nécessaire pour utiliser cette commande.")
    else:
        await ctx.send("⚠️ Une erreur inconnue s'est produite.")

#---------------------------------------- Rage du Berserker

BerserkCooldown = {}

@bot.command(name="berserk")
@commands.cooldown(1, 604800, commands.BucketType.user)  # 7 jours cooldown
async def berserk(ctx, target: discord.Member = None):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")

    # Check rôle
    if RAGE_ID not in [role.id for role in ctx.author.roles]:
        return await ctx.send("Tu n'as pas le rôle nécessaire pour utiliser cette commande.")

    if target is None or target.bot or target == ctx.author:
        return await ctx.send("Tu dois cibler un autre utilisateur valide.")

    guild_id = ctx.guild.id
    author_id = ctx.author.id
    target_id = target.id

    roll = random.randint(1, 100)

    # Récupération des données
    author_data = get_or_create_user_data(guild_id, author_id)
    target_data = get_or_create_user_data(guild_id, target_id)

    result = ""
    image_url = "https://github.com/Iseyg91/Isey_aime_Cass/blob/main/unnamed.jpg?raw=true"

    # Logique du roll
    if roll <= 10:
        perte = int(author_data["bank"] * 0.15)
        collection.update_one({"guild_id": guild_id, "user_id": author_id}, {"$inc": {"bank": -perte}})
        result = f"🎲 Roll: {roll}\n⚠️ L’armure se retourne contre toi ! Tu perds **15%** de ta propre banque soit **{perte:,}**."

    elif roll == 100:
        perte = target_data["bank"]
        collection.update_one({"guild_id": guild_id, "user_id": target_id}, {"$inc": {"bank": -perte}})

        eclipse_role = ctx.guild.get_role(ECLIPSE_ROLE_ID)
        if eclipse_role:
            try:
                await ctx.author.add_roles(eclipse_role)
            except discord.Forbidden:
                await ctx.send("❌ Je n’ai pas les permissions pour te donner le rôle Éclipse.")
            except Exception as e:
                await ctx.send(f"❌ Une erreur est survenue lors de l’ajout du rôle : {e}")
        else:
            await ctx.send("⚠️ Le rôle Éclipse n’a pas été trouvé sur le serveur.")

        result = (
            f"🎲 Roll: {roll}\n💥 **Effet Éclipse !**\n"
            f"→ {target.mention} perd **100%** de sa banque soit **{perte:,}**.\n"
            f"→ Tu deviens **L’incarnation de la Rage**."
        )

    else:
        perte = int(target_data["bank"] * (roll / 100))
        collection.update_one({"guild_id": guild_id, "user_id": target_id}, {"$inc": {"bank": -perte}})
        result = (
            f"🎲 Roll: {roll}\n🎯 {target.mention} perd **{roll}%** de sa banque soit **{perte:,}**.\n"
            f"Tu ne gagnes rien. Juste le chaos."
        )

    # Embed du résultat
    embed = discord.Embed(title="🔥 Berserk Activé ! 🔥", description=result, color=discord.Color.red())
    embed.set_image(url=image_url)
    embed.set_footer(text=f"Par {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

@berserk.error
async def berserk_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = datetime.timedelta(seconds=error.retry_after)
        await ctx.send(f"⏳ Cette commande est en cooldown. Réessaie dans {cooldown}.")
    else:
        raise error

#--------------------------------------------------------------- Armure

@bot.command()
async def armure(ctx):
    # Vérifie si l'utilisateur a le rôle d'armure
    if ARMURE_ID in [role.id for role in ctx.author.roles]:
        # Retirer immédiatement le rôle d'armure
        armure_role = discord.utils.get(ctx.guild.roles, id=ARMURE_ID)
        await ctx.author.remove_roles(armure_role)
        
        # Ajouter le rôle anti-rob
        anti_rob_role = discord.utils.get(ctx.guild.roles, id=ANTI_ROB_ID)
        await ctx.author.add_roles(anti_rob_role)
        
        # Créer l'embed
        embed = Embed(
            title="Anti-Rob Activé",
            description="Vous avez reçu un anti-rob pour 1 heure !",
            color=discord.Color.green()
        )
        embed.set_image(url="https://miro.medium.com/v2/resize:fit:1024/0*wATbQ49jziZTyhZH.jpg")
        
        # Envoyer l'embed
        await ctx.send(embed=embed)

        # Attendre 1 heure (3600 secondes)
        await asyncio.sleep(3600)

        # Retirer le rôle anti-rob après 1 heure
        await ctx.author.remove_roles(anti_rob_role)
        await ctx.send(f"L'anti-rob de {ctx.author.mention} a expiré.")
    else:
        await ctx.send("Vous n'avez pas le rôle nécessaire pour utiliser cette commande.")

#------------------------------------------------ Infini
# Lien des images selon le niveau
images = {
    1: "https://preview.redd.it/zovgpfd6g6od1.jpeg?auto=webp&s=59768167ffc7b8d39072709119686464e7cbddff",
    2: "https://i0.wp.com/www.lerenardmasque.com/wp-content/uploads/2023/08/Capture-decran-2023-08-16-a-13.29.09.png?resize=960%2C419&ssl=1",
    3: "https://i0.wp.com/www.lerenardmasque.com/wp-content/uploads/2023/08/Capture-decran-2023-08-16-a-13.34.03-1.png?resize=960%2C498&ssl=1"
}

# Dictionnaire pour stocker le temps d'expiration de chaque utilisateur
user_anti_rob_expiry = {}

# Commande .infini
@bot.command()
async def infini(ctx):
    member = ctx.author
    current_time = datetime.utcnow()

    # Vérifier si l'utilisateur a déjà un anti-rob actif
    if member.id in user_anti_rob_expiry:
        expiry_time = user_anti_rob_expiry[member.id]
        if current_time < expiry_time:
            remaining_time = expiry_time - current_time
            await ctx.send(f"Vous avez déjà un anti-rob actif. Il expire dans {str(remaining_time).split('.')[0]}.")
            return

    roles = member.roles

    # Vérification des rôles et assignation de l'anti-rob
    for role_id in INFINI_ID:
        role = discord.utils.get(roles, id=role_id)
        if role:
            if role.id == INFINI_ID[0]:
                anti_rob_duration = 1  # 1h pour Niv 1
                image_url = images[1]
            elif role.id == INFINI_ID[1]:
                anti_rob_duration = 3  # 3h pour Niv 2
                image_url = images[2]
            elif role.id == INFINI_ID[2]:
                anti_rob_duration = 6  # 6h pour Niv 3
                image_url = images[3]
            
            # Retirer immédiatement le rôle INFINI_ID
            await member.remove_roles(role)
            print(f"Rôle {role.name} retiré de {member.name}")

            # Ajouter le rôle anti-rob
            anti_rob_role = discord.utils.get(member.guild.roles, id=ANTI_ROB_ROLE)
            await member.add_roles(anti_rob_role)
            print(f"Rôle anti-rob ajouté à {member.name}")

            # Enregistrer l'heure d'expiration de l'anti-rob
            expiry_time = current_time + timedelta(hours=anti_rob_duration)
            user_anti_rob_expiry[member.id] = expiry_time

            # Créer un embed pour afficher le message
            embed = discord.Embed(title="Anti-Rob Activé", description=f"Vous avez reçu un anti-rob de {anti_rob_duration} heure(s).", color=0x00ff00)
            embed.set_image(url=image_url)
            embed.timestamp = current_time

            # Envoyer le message avec l'embed
            await ctx.send(embed=embed)
            break
    else:
        await ctx.send("Vous n'avez pas le rôle nécessaire pour utiliser cette commande.")

#----------------------------------------- Pokeball
# Limite d'utilisation par semaine
last_used = {}

# Fonction pour vérifier l'accès basé sur le rôle
async def has_authorized_role(user):
    return any(role.id == POKEBALL_ID for role in user.roles)

# Commande pokeball
@bot.command(name="pokeball", description="Permet de voler un objet à une personne spécifique.")
async def pokeball(ctx, target: discord.Member = None):
    user = ctx.author
    
    # Vérifier si l'utilisateur a le bon rôle
    if not await has_authorized_role(user):
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
        return
    
    # Vérifier la limite d'utilisation hebdomadaire
    current_time = datetime.now()
    if user.id in last_used:
        time_diff = current_time - last_used[user.id]
        if time_diff < timedelta(weeks=1):
            await ctx.send("Vous avez déjà utilisé cette commande cette semaine. Réessayez plus tard.")
            return
    
    # Si aucune cible n'est spécifiée, l'utilisateur doit mentionner un membre
    if target is None:
        await ctx.send("Veuillez mentionner un membre à qui voler un objet.")
        return
    
    # Vérifier que la cible n'est pas un bot
    if target.bot:
        await ctx.send("Vous ne pouvez pas voler des objets à un bot.")
        return
    
    # Récupérer l'inventaire de l'utilisateur choisi
    guild = ctx.guild
    items_cursor = collection17.find({"guild_id": guild.id, "user_id": target.id})
    items = list(items_cursor)

    if not items:
        await ctx.send(f"{target.name} n'a pas d'objets dans son inventaire.")
        return

    # Voler un objet au hasard
    stolen_item = random.choice(items)
    item_name = stolen_item.get("item_name", "Nom inconnu")
    item_emoji = stolen_item.get("emoji", "")
    
    # Supprimer l'objet volé de l'inventaire de la victime
    collection17.delete_one({"_id": stolen_item["_id"]})
    
    # Ajouter l'objet volé à l'inventaire de l'utilisateur
    collection17.insert_one({
        "guild_id": guild.id,
        "user_id": user.id,
        "item_id": stolen_item["item_id"],
        "item_name": item_name,
        "emoji": item_emoji
    })

    # Mettre à jour la dernière utilisation
    last_used[user.id] = current_time
    
    # Embed de la réponse
    embed = discord.Embed(
        title="Pokeball utilisée avec succès !",
        description=f"Vous avez volé **1x {item_name} {item_emoji}** à {target.name}.",
        color=discord.Color.green()
    )
    embed.set_image(url="https://fr.web.img2.acsta.net/newsv7/20/03/19/15/11/26541590.jpg")
    embed.set_footer(text="Utilisation 1x par semaine.")
    
    await ctx.send(embed=embed)

#--------------------------------------------- Float
# Maintenant, vous pouvez utiliser timedelta directement
COOLDOWN_TIME = timedelta(days=1)

# Dictionnaire pour stocker le dernier usage de la commande .float par utilisateur
float_last_used = {}

# URL de l'image
image_url = "https://preview.redd.it/vczetgcwdrge1.jpeg?auto=webp&s=7c04e8249d0ee9f8e231c5940aafecb7a2c5a2ca"

@bot.command()
async def float(ctx):
    # Vérifie si l'utilisateur a le bon rôle
    if FLOAT_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("Tu n'as pas le rôle nécessaire pour utiliser cette commande.")
        return
    
    current_time = datetime.datetime.now()
    last_used_time = float_last_used.get(ctx.author.id)

    # Vérifie si l'utilisateur a déjà utilisé la commande dans les dernières 24 heures
    if last_used_time and current_time - last_used_time < COOLDOWN_TIME:
        await ctx.send("Tu as déjà utilisé cette commande aujourd'hui. Patiente avant de réessayer.")
        return

    # Ajoute le rôle nécessaire à l'utilisateur
    role = ctx.guild.get_role(ROLE_FLOAT_ID)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, tu as maintenant accès au salon pendant 15 minutes.")
        
        # Envoie l'embed avec l'image
        embed = discord.Embed(
            title="Utilisation du pouvoir de Nana Shimura",
            description="Tu as utilisé un des alters de One for All et tu accèdes au salon pendant 15 minutes.",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

        # Met à jour le dernier usage de la commande
        float_last_used[ctx.author.id] = current_time

        # Programme la suppression du rôle après 15 minutes
        await asyncio.sleep(15 * 60)
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, ton accès au salon est maintenant terminé.")
    else:
        await ctx.send("Le rôle nécessaire n'a pas pu être trouvé.")

#------------------------------------- Oeil Demoniaque

COOLDOWN_TIME = timedelta(weeks=1)

# Dictionnaire pour stocker le dernier usage de la commande .oeil par utilisateur
oeil_last_used = {}

# URL de l'image
image_url = "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2023/09/rudeus-demon-eye-mushoku-tensei.jpg"

@bot.command()
async def oeil(ctx):
    # Vérifie si l'utilisateur a le bon rôle
    if OEIL_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("Tu n'as pas le rôle nécessaire pour utiliser cette commande.")
        return
    
    current_time = datetime.datetime.now()
    last_used_time = oeil_last_used.get(ctx.author.id)

    # Vérifie si l'utilisateur a déjà utilisé la commande dans les dernières 1 semaine
    if last_used_time and current_time - last_used_time < COOLDOWN_TIME:
        await ctx.send("Tu as déjà utilisé cette commande cette semaine. Patiente avant de réessayer.")
        return

    # Ajoute le rôle nécessaire à l'utilisateur
    role = ctx.guild.get_role(ROLE_ID)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, tu as utilisé le pouvoir de Kishirika pour voir l'avenir pendant 10 secondes.")
        
        # Envoie l'embed avec l'image
        embed = discord.Embed(
            title="Le pouvoir de Kishirika",
            description="Tu entrevois le prochain restock pendant 10 secondes grâce au pouvoir de Kishirika.",
            color=discord.Color.purple()
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

        # Met à jour le dernier usage de la commande
        oeil_last_used[ctx.author.id] = current_time

        # Programme la suppression du rôle après 10 secondes
        await asyncio.sleep(10)
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, ton accès au pouvoir de voir l'avenir est maintenant terminé.")

    else:
        await ctx.send("Le rôle nécessaire n'a pas pu être trouvé.")

#---------------------------------------------- Benediction

@bot.command(name="benediction")
async def benediction(ctx):
    user_id = ctx.author.id
    guild_id = ctx.guild.id
    now = datetime.utcnow()

    # Vérifie si l'utilisateur a le rôle requis
    if BENEDICTION_ROLE_ID not in [role.id for role in ctx.author.roles]:
        embed = discord.Embed(
            title="❌ Accès refusé",
            description="Tu n'as pas le rôle nécessaire pour recevoir la bénédiction d'Etherya.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    # Récupère un item aléatoire de la boutique (en stock uniquement, et pas interdit)
    items = list(collection16.find({
        "quantity": {"$gt": 0},
        "id": {"$nin": ITEMS_INTERDITS}
    }))
    
    if not items:
        embed = discord.Embed(
            title="❌ Aucun item disponible",
            description="Il n'y a pas d'items à matérialiser actuellement.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    selected_item = random.choice(items)

    # Met à jour l'inventaire simple
    existing = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
    if existing:
        inventory = existing.get("items", {})
        inventory[str(selected_item["id"])] = inventory.get(str(selected_item["id"]), 0) + 1
        collection7.update_one(
            {"user_id": user_id, "guild_id": guild_id},
            {"$set": {"items": inventory}}
        )
    else:
        collection7.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "items": {str(selected_item["id"]): 1}
        })

    # Ajoute à l'inventaire structuré
    collection17.insert_one({
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": selected_item["id"],
        "item_name": selected_item["title"],
        "emoji": selected_item.get("emoji"),
        "price": selected_item["price"],
        "obtained_at": now
    })

    # Retire le rôle après utilisation
    role = discord.utils.get(ctx.guild.roles, id=BENEDICTION_ROLE_ID)
    if role:
        await ctx.author.remove_roles(role)

    # Message de confirmation avec image et texte modifié
    embed = discord.Embed(
        title="🌟 Bénédiction d'Etherya",
        description=(
            "La bénédiction d'Etherya t'a été accordée ! **La Divinité t'a offert un cadeau précieux pour "
            "ta quête. Que ce pouvoir guide tes pas vers la victoire !**\n\n"
            f"Tu as reçu **{selected_item['emoji']} {selected_item['title']}** pour ta bravoure et ta foi."
        ),
        color=discord.Color.green()
    )
    embed.set_image(url="https://imgsrv.crunchyroll.com/cdn-cgi/image/fit=contain,format=auto,quality=70,width=1200,height=675/catalog/crunchyroll/59554268b0e9e3e565547ab4e25453f4.jpg")
    await ctx.send(embed=embed)

#---------------------------------------------------- Bounty & Honor

# Fonction pour récupérer la prime
async def get_bounty(user_id):
    bounty = collection37.find_one({"user_id": user_id})
    return bounty['prime'] if bounty else 50

# Fonction pour récupérer l'honneur
async def get_honor(user_id):
    honor = collection38.find_one({"user_id": user_id})
    return honor['honor'] if honor else 50

@bot.command()
async def bounty(ctx):
    pirate_role_id = 1365682636957421741

    # Vérifier si l'utilisateur a le rôle Pirate
    if pirate_role_id not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ Vous n'avez pas l'autorisation d'utiliser cette commande.")
        return

    user = ctx.author
    user_id = user.id
    bounty = await get_bounty(user_id)

    # Créer l'embed personnalisé
    embed = Embed(
        title="🏴‍☠️ Feuille de Prime",
        description=(
            f"💰 **Prime actuelle** : **{bounty}**\n"
            f"⚠️ Statut : Pirate recherché vivant ou mort\n"
            f"📅 Dernière mise à jour : aujourd'hui\n\n"
            f"Continuez vos méfaits... ou surveillez vos arrières. 🩸"
        ),
        color=0x8B0000  # Rouge foncé style sang
    )

    # Nom + PP en haut à gauche
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

    # Footer stylisé
    embed.set_footer(text="Empire Pirate • Commande /bounty", icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

    # Envoi en message privé
    await user.send(embed=embed)

@bot.command()
async def honor(ctx):
    marine_role_id = 1365631932964012142

    # Vérifie si l'utilisateur a le rôle requis
    if any(role.id == marine_role_id for role in ctx.author.roles):
        user = ctx.author
        user_id = user.id
        honor = await get_honor(user_id)

        # Crée un embed stylisé
        embed = Embed(
            title="📜 Rapport d'Honneur",
            description=(
                f"🎖️ **Honneur actuel** : **{honor}**\n"
                f"🔹 Statut : Membre loyal de la Marine\n"
                f"📅 Dernière inspection : aujourd'hui\n\n"
                f"Continuez à servir avec fierté et discipline. 💙"
            ),
            color=0x003366  # Bleu marine
        )

        # Affiche la PP en haut à gauche + nom complet
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

        # Footer avec le tag + icône
        embed.set_footer(text="Gloire à la Marine • Commande /honor", icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

        # Envoi en message privé
        await user.send(embed=embed)
    else:
        await ctx.send("❌ Vous n'avez pas le rôle requis pour utiliser cette commande.")

# Fonction pour récupérer la prime
async def get_bounty(user_id):
    bounty = collection37.find_one({"user_id": user_id})
    return bounty['prime'] if bounty else 50

# Fonction pour récupérer l'honneur
async def get_honor(user_id):
    honor = collection38.find_one({"user_id": user_id})
    return honor['honor'] if honor else 50

task_annonce_jour = None  # Déclaration globale de la tâche

async def annonce_jour():
    while True:
        print("Annonce du jour")  # À remplacer par ton vrai comportement
        await asyncio.sleep(86400)  # Une fois par jour

async def start_background_tasks():
    global task_annonce_jour
    if not task_annonce_jour or task_annonce_jour.done():
        task_annonce_jour = asyncio.create_task(annonce_jour())

async def capture_user(ctx, captor_id, target_id, captor_roles, target_roles, target):
    captor_bounty = await get_bounty(captor_id)
    target_bounty = await get_bounty(target_id)

    # Vérifier si la capture peut se faire (pirate ou marine)
    captor_is_pirate = any(role.id == ISEY_PIRATE_ID for role in captor_roles)
    target_is_pirate = any(role.id == ISEY_PIRATE_ID for role in target_roles)

    captor_is_marine = any(role.id == ISEY_MARINE_ID for role in captor_roles)
    target_is_marine = any(role.id == ISEY_MARINE_ID for role in target_roles)

    # Un pirate peut capturer un pirate ou un marine et inversement
    if not (captor_is_pirate and (target_is_pirate or target_is_marine)) and not (captor_is_marine and target_is_pirate):
        await ctx.send("Les pirates peuvent capturer les pirates et les marines, et les marines peuvent capturer les pirates.")
        return

    # Cooldown
    cooldown_data = collection39.find_one({"user_id": captor_id})
    if cooldown_data and datetime.utcnow() < cooldown_data["next_capture"]:
        time_remaining = cooldown_data["next_capture"] - datetime.utcnow()
        await ctx.send(f"Vous devez attendre encore {time_remaining} avant de capturer quelqu'un.")
        return

    # Chances de réussite
    success_chance = max(0.1, 1 - (target_bounty / 200))
    if random.random() > success_chance:
        await ctx.send(f"{ctx.author.name} a tenté de capturer {target.name}, mais la capture a échoué.")
        return

    # Gestion des primes
    if target_bounty > captor_bounty:
        loss = target_bounty // 2
        gain = loss
        collection37.update_one({"user_id": captor_id}, {"$inc": {"prime": -loss}}, upsert=True)
        collection37.update_one({"user_id": target_id}, {"$inc": {"prime": gain}}, upsert=True)
        await ctx.send(f"{ctx.author.name} a capturé {target.name}, il a perdu {loss} de prime et {target.name} a gagné {gain} de prime.")
    else:
        await ctx.send(f"{ctx.author.name} a capturé {target.name}, mais rien n'a changé car les primes sont égales ou {ctx.author.name} a plus de prime.")

    # Mise à jour du cooldown
    cd_capture_ether_collection.update_one(
        {"user_id": captor_id},
        {"$set": {"next_capture": datetime.utcnow() + timedelta(hours=12)}},
        upsert=True
    )

@bot.command()
async def capture(ctx, target: discord.Member):
    captor_id = ctx.author.id
    target_id = target.id

    allowed_roles = [ISEY_PIRATE_ID, ISEY_MARINE_ID]
    author_roles_ids = [role.id for role in ctx.author.roles]

    # Debug : Afficher les rôles pour vérification
    print(f"Rôles de l'auteur : {author_roles_ids}")
    
    if not any(role_id in allowed_roles for role_id in author_roles_ids):
        await ctx.send("Vous devez avoir un rôle autorisé pour capturer des cibles.")
        return

    captor_roles = ctx.author.roles
    target_roles = target.roles

    # Vérification des rôles pour la capture
    if any(role.id == ISEY_PIRATE_ID for role in captor_roles) or any(role.id == ISEY_MARINE_ID for role in captor_roles):
        await capture_user(ctx, captor_id, target_id, captor_roles, target_roles, target)
    else:
        await ctx.send("Seuls les pirates et marines peuvent capturer des cibles.")

# Commande pour réinitialiser la collection bounty (collection 37)
@bot.command()
async def reset_bounty(ctx):
    # Vérifier si l'utilisateur est ISEY_ID
    if ctx.author.id != ISEY_ID:
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
        return
    
    # Réinitialisation de la collection bounty (collection 37)
    collection37.delete_many({})  # Nettoyer la collection bounty
    await ctx.send("La collection des primes a été réinitialisée avec succès.")

# Commande pour réinitialiser la collection honor (collection 38)
@bot.command()
async def reset_prime(ctx):
    # Vérifier si l'utilisateur est ISEY_ID
    if ctx.author.id != ISEY_ID:
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
        return
    
    # Réinitialisation de la collection honor (collection 38)
    collection38.delete_many({})  # Nettoyer la collection honor
    await ctx.send("La collection des honneurs a été réinitialisée avec succès.")

#----------------------------------------- Baku baku no Mi
@bot.command()
async def bombe(ctx, target: discord.Member = None):
    author_id = ctx.author.id

    # Vérification du rôle
    if BOMBE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ Tu n'as pas le rôle requis pour utiliser cette commande.")
        # Log : l'utilisateur n'a pas le rôle requis
        await log_eco_channel(
            bot, ctx.guild.id, ctx.author,
            action="🔴 Tentative d'utilisation non autorisée de la commande Bombe",
            note=f"Tenté par {ctx.author.name}, ID {author_id}"
        )
        return

    # Vérification si un membre est ciblé
    if target is None:
        await ctx.send("❌ Tu dois spécifier un membre à cibler.")
        # Log : Aucun membre ciblé
        await log_eco_channel(
            bot, ctx.guild.id, ctx.author,
            action="🛑 Aucune cible spécifiée pour la Bombe",
            note=f"Tenté par {ctx.author.name}, ID {author_id}"
        )
        return

    guild_id = ctx.guild.id
    user_id = target.id

    # Vérification du cooldown
    cooldown_data = collection40.find_one({"guild_id": guild_id, "user_id": user_id})
    now = datetime.utcnow()

    if cooldown_data and now < cooldown_data["used_at"] + timedelta(days=7):
        next_use = cooldown_data["used_at"] + timedelta(days=7)
        remaining = next_use - now
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes = remainder // 60
        await ctx.send(f"🕒 Ce joueur a déjà été bombardé récemment. Réessaye dans {hours}h{minutes}m.")
        # Log : Tentative pendant cooldown
        await log_eco_channel(
            bot, guild_id, ctx.author,
            action="🔁 Tentative de bombe pendant le cooldown",
            note=f"Tenté par {ctx.author.name} sur {target.name}, cooldown jusqu'à {next_use.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return

    # Récupération des données du joueur ciblé
    target_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not target_data:
        await ctx.send("❌ Ce joueur n'a pas de données économiques.")
        # Log : Aucune donnée économique pour la cible
        await log_eco_channel(
            bot, guild_id, ctx.author,
            action="🚫 Aucune donnée économique pour la cible",
            note=f"Aucune donnée trouvée pour {target.name} (ID {user_id})"
        )
        return

    bank_before = target_data.get("bank", 0)
    amount_to_remove = int(bank_before * 0.10)
    new_bank = bank_before - amount_to_remove

    # Mise à jour de la banque
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"bank": new_bank}}
    )

    # Mise à jour du cooldown
    collection40.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"used_at": now}},
        upsert=True
    )

    # Log : Action réussie
    await log_eco_channel(
        bot, guild_id, target,
        action="💣 Bombe économique",
        amount=amount_to_remove,
        balance_before=f"{bank_before} en banque",
        balance_after=f"{new_bank} en banque",
        note=f"Par {ctx.author.name}"
    )

    # Embed de retour
    embed = discord.Embed(
        title="💥 Explosion Économique !",
        description=f"{ctx.author.mention} a largué une **bombe** sur {target.mention} !\n"
                    f"💸 **10%** de sa banque ont été volés : **{amount_to_remove:,}** <:ecoEther:1341862366249357374>",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/onepiece/images/8/86/Bomu_Bomu_no_Mi_Anime_Infobox.png/revision/latest?cb=20181120231615&path-prefix=fr")
    await ctx.send(embed=embed)

#------------------------------------------------- Gura Gura no Mi
@bot.command(name="gura")
@commands.guild_only()
async def gura(ctx, target: discord.Member = None):
    role_required = 1365313248269828116
    cooldown_weeks = 3

    # Vérifie si l'auteur a le rôle requis
    if role_required not in [role.id for role in ctx.author.roles]:
        logging.warning(f"{ctx.author} n'a pas le rôle requis pour invoquer un séisme.")
        return await ctx.send("🚫 Tu n'as pas la puissance nécessaire pour invoquer un séisme destructeur.")

    # Vérifie si un utilisateur cible a été mentionné
    if target is None:
        logging.warning(f"{ctx.author} n'a pas ciblé de membre pour le séisme.")
        return await ctx.send("🚫 Tu dois mentionner un utilisateur pour utiliser cette commande.")

    user_id = ctx.author.id
    guild_id = ctx.guild.id

    # Vérification du cooldown
    cd_data = collection41.find_one({"user_id": user_id, "guild_id": guild_id})
    now = datetime.utcnow()

    if cd_data:
        last_used = cd_data.get("last_used", now - timedelta(weeks=cooldown_weeks + 1))
        if now - last_used < timedelta(weeks=cooldown_weeks):
            remaining = timedelta(weeks=cooldown_weeks) - (now - last_used)
            logging.info(f"{ctx.author} essaie d'utiliser le Gura Gura no Mi avant la fin du cooldown.")
            return await ctx.send(f"🕒 Tu dois encore attendre `{str(remaining).split('.')[0]}` avant de pouvoir utiliser à nouveau le **Gura Gura no Mi**.")
    
    # Mise à jour du cooldown
    collection41.update_one(
        {"user_id": user_id, "guild_id": guild_id},
        {"$set": {"last_used": now}},
        upsert=True
    )

    # Embed RP
    embed = discord.Embed(
        title="🌊 Gura Gura no Mi - Séisme Déclenché !",
        description=(
            f"**{ctx.author.mention}** a libéré une onde sismique destructrice contre **{target.mention}** !\n\n"
            "Les fondations de la banque tremblent... les coffres s'effondrent sous la puissance du fruit du tremblement !"
        ),
        color=discord.Color.dark_red(),
        timestamp=now
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/onepiece/images/3/38/Gura_Gura_no_Mi_Anime_Infobox.png/revision/latest?cb=20130509112508&path-prefix=fr")
    embed.set_footer(text="Cooldown: 3 semaines")

    await ctx.send(embed=embed)
    logging.info(f"{ctx.author} a utilisé le Gura Gura no Mi contre {target}.")

#------------------------------------------------------------ Hie Hie no Mi (Fruit de la Glace)
# Durées
DUREE_COOLDOWN = timedelta(weeks=1)
DUREE_GEL = timedelta(days=3)

@bot.command(name="glace")
@commands.guild_only()
async def glace(ctx, cible: discord.Member = None):
    auteur = ctx.author

    # Vérification du rôle autorisé
    if ROLE_UTILISATEUR_GLACE not in [r.id for r in auteur.roles]:
        await ctx.send("❌ Tu n'as pas le rôle requis pour utiliser cette commande.")
        # Log: Rôle non autorisé
        print(f"[LOG] {auteur.display_name} ({auteur.id}) a tenté d'utiliser .glace sans le rôle requis.")
        return

    # Vérifier si l'utilisateur a ciblé quelqu'un
    if not cible:
        await ctx.send("❌ Tu dois mentionner un membre à geler.")
        # Log: Pas de cible mentionnée
        print(f"[LOG] {auteur.display_name} ({auteur.id}) a utilisé .glace sans spécifier de cible.")
        return

    # Vérifier si la cible est la même que l'auteur
    if cible == auteur:
        await ctx.send("❌ Tu ne peux pas te geler toi-même.")
        # Log: Tentative de gel sur soi-même
        print(f"[LOG] {auteur.display_name} ({auteur.id}) a tenté de se geler lui-même.")
        return

    # Vérifier si l'utilisateur est en cooldown
    cooldown_data = collection42.find_one({"user_id": auteur.id})
    now = datetime.utcnow()

    if cooldown_data and cooldown_data["timestamp"] > now:
        remaining = cooldown_data["timestamp"] - now
        await ctx.send(f"⏳ Tu dois attendre encore {remaining.days}j {remaining.seconds//3600}h avant de pouvoir utiliser `.glace` à nouveau.")
        # Log: Utilisateur en cooldown
        print(f"[LOG] {auteur.display_name} ({auteur.id}) a tenté d'utiliser .glace en cooldown.")
        return

    # Appliquer le rôle de gel à la cible
    role = discord.utils.get(ctx.guild.roles, id=ROLE_GEL)
    if not role:
        await ctx.send("❌ Rôle de gel introuvable sur ce serveur.")
        # Log: Rôle de gel non trouvé
        print("[LOG] Rôle de gel introuvable sur le serveur.")
        return
    
    try:
        await cible.add_roles(role, reason="Gel économique via .glace")
        # Log: Rôle de gel ajouté
        print(f"[LOG] Rôle de gel ajouté à {cible.display_name} ({cible.id}) par {auteur.display_name} ({auteur.id}).")
    except discord.Forbidden:
        await ctx.send("❌ Impossible d'ajouter le rôle à cet utilisateur.")
        # Log: Erreur d'ajout de rôle
        print(f"[LOG] {auteur.display_name} ({auteur.id}) n'a pas pu ajouter le rôle de gel à {cible.display_name} ({cible.id}) - Permission refusée.")
        return

    # Enregistrer le cooldown dans Mongo
    collection42.update_one(
        {"user_id": auteur.id},
        {"$set": {"timestamp": now + DUREE_COOLDOWN}},
        upsert=True
    )

    # Enregistrer la fin du gel de la cible
    collection43.update_one(
        {"user_id": cible.id},
        {"$set": {"remove_at": now + DUREE_GEL}},
        upsert=True
    )

    # Embed d'information
    embed = discord.Embed(
        title="❄️ Gel économique !",
        description=f"{cible.mention} est gelé pendant **3 jours** !",
        color=discord.Color.blue(),
        timestamp=now
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/onepiece/images/9/9b/Hie_Hie_no_Mi_Anime_Infobox.png/revision/latest?cb=20160604184118&path-prefix=fr")
    embed.set_footer(text=f"L'utilisateur {auteur.display_name} a utilisé le pouvoir de la Glace.")
    
    await ctx.send(embed=embed)
    # Log: Action réussie
    print(f"[LOG] {auteur.display_name} ({auteur.id}) a utilisé .glace sur {cible.display_name} ({cible.id}).")

#----------------------------------------------- Yami Yami no Mi
@bot.command(name="tenebre")
@commands.has_role(1365313251201519697)
async def tenebre(ctx):
    user_id = ctx.author.id
    now = datetime.utcnow()

    # Vérifie si l'utilisateur a le rôle requis
    if not any(role.id == 1365313251201519697 for role in ctx.author.roles):
        await ctx.send("🚫 Tu n'as pas le rôle nécessaire pour utiliser cette capacité.")
        # Log si l'utilisateur n'a pas le rôle
        print(f"{now} - {ctx.author} n'a pas le rôle requis pour utiliser la commande tenebre.")
        return

    # Vérifie le cooldown de 24h
    cd_doc = collection44.find_one({"user_id": user_id})
    if cd_doc and (now - cd_doc["last_use"]).total_seconds() < 86400:
        remaining = timedelta(seconds=86400 - (now - cd_doc["last_use"]).total_seconds())
        await ctx.send(f"⏳ Tu dois encore attendre {remaining} avant de réutiliser cette capacité.")
        # Log pour cooldown
        print(f"{now} - {ctx.author} essaie d'utiliser la commande tenebre avant la fin du cooldown.")
        return

    # Ajoute ou met à jour le cooldown
    collection44.update_one(
        {"user_id": user_id},
        {"$set": {"last_use": now}},
        upsert=True
    )
    # Log de mise à jour du cooldown
    print(f"{now} - {ctx.author} a utilisé la commande tenebre. Cooldown mis à jour.")

    # Ajoute la protection de 6h contre les robs
    collection45.update_one(
        {"user_id": user_id},
        {"$set": {"protection_start": now}},
        upsert=True
    )
    # Log de protection ajoutée
    print(f"{now} - {ctx.author} a activé la protection contre les robs pour 6h.")

    # Donne le rôle temporaire (3 jours)
    role_id = 1365313254108430396
    role = ctx.guild.get_role(role_id)
    if role:
        await ctx.author.add_roles(role)
        await asyncio.sleep(259200)  # 3 jours en secondes
        await ctx.author.remove_roles(role)
        # Log de l'ajout et retrait du rôle
        print(f"{now} - {ctx.author} a reçu le rôle des ténèbres pendant 3 jours.")

    # Embed de confirmation
    embed = discord.Embed(
        title="🌑 Pouvoir des Ténèbres activé !",
        description="Tu as activé le **Yami Yami no Mi**.\nTu renverras **200%** des vols et es **protégé pendant 6h** contre les tentatives de vol.",
        color=discord.Color.dark_purple()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/onepiece/images/1/1f/Yami_Yami_no_Mi_Anime_Infobox.png/revision/latest?cb=20130221181805&path-prefix=fr")
    embed.set_footer(text="Effets du fruit des ténèbres")
    await ctx.send(embed=embed)

    # Log de succès
    print(f"{now} - {ctx.author} a utilisé la commande tenebre avec succès. Rôle et protection activés.")

#---------------------------------------------- Gomu Gomu no Mi
@bot.command()
async def gearsecond(ctx):
    # Vérifier si l'utilisateur a le rôle requis
    role_id = 1365311611019202744
    role = discord.utils.get(ctx.author.roles, id=role_id)
    if not role:
        await ctx.send("Tu n'as pas le rôle requis pour utiliser cette commande.")
        print(f"[LOG] {ctx.author} n'a pas le rôle requis pour utiliser Gear Second.")
        return

    # Vérifier si l'utilisateur a un cooldown
    cooldown_data = collection46.find_one({"user_id": ctx.author.id})
    if cooldown_data:
        last_used = cooldown_data["last_used"]
        cooldown_end = last_used + timedelta(weeks=2)
        if datetime.utcnow() < cooldown_end:
            await ctx.send(f"Tu dois attendre encore {cooldown_end - datetime.utcnow()} avant de réutiliser cette commande.")
            print(f"[LOG] {ctx.author} a essayé d'utiliser Gear Second avant la fin du cooldown.")
            return

    # Ajouter le cooldown de 2 semaines
    collection46.update_one(
        {"user_id": ctx.author.id},
        {"$set": {"last_used": datetime.utcnow()}},
        upsert=True
    )
    print(f"[LOG] Cooldown mis à jour pour {ctx.author} à {datetime.utcnow()}.")

    # Ajouter le rôle à l'utilisateur
    gear_second_role_id = 1365313261129568297
    gear_second_role = discord.utils.get(ctx.guild.roles, id=gear_second_role_id)
    await ctx.author.add_roles(gear_second_role)
    
    # Retirer le rôle après 1 semaine
    await ctx.send(f"Tu as activé le Gear Second, {ctx.author.mention} ! Ton rôle sera retiré dans 1 semaine.")
    print(f"[LOG] {ctx.author} a activé Gear Second.")

    # Enlever le rôle après 1 semaine
    await discord.utils.sleep_until(datetime.utcnow() + timedelta(weeks=1))
    await ctx.author.remove_roles(gear_second_role)
    print(f"[LOG] {ctx.author} a perdu le rôle Gear Second après 1 semaine.")

    # Envoyer un embed avec l'image
    embed = discord.Embed(
        title="Gear Second Activé",
        description="Tu as activé ton mode Gear Second pour une semaine !",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.set_image(url="https://www.univers-otaku.com/wp-content/uploads/2021/06/Luffy-Gear-2nd-vs-Blueno.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def gearfourth(ctx):
    # Vérifier si l'utilisateur a le bon rôle
    if not any(role.id == 1365311611019202744 for role in ctx.author.roles):
        await ctx.send("Désolé, tu n'as pas le rôle nécessaire pour utiliser cette commande.")
        # Log : L'utilisateur n'a pas le rôle requis
        print(f"[LOG] {ctx.author} a tenté d'utiliser la commande gearfourth sans avoir le rôle nécessaire.")
        return

    # Vérifier le cooldown
    cooldown_data = collection47.find_one({"user_id": ctx.author.id})
    if cooldown_data:
        last_used = cooldown_data.get("last_used")
        if last_used:
            cooldown_end = last_used + datetime.timedelta(days=7)
            if datetime.datetime.utcnow() < cooldown_end:
                time_remaining = str(cooldown_end - datetime.datetime.utcnow()).split('.')[0]
                await ctx.send(f"Tu dois attendre encore {time_remaining} avant de pouvoir réutiliser cette commande.")
                # Log : L'utilisateur est en cooldown
                print(f"[LOG] {ctx.author} a tenté d'utiliser la commande gearfourth, mais est en cooldown jusqu'à {cooldown_end}.")
                return
    
    # Ajouter le rôle Gear Fourth
    gearfourth_role = discord.utils.get(ctx.guild.roles, id=1365313284584116264)
    await ctx.author.add_roles(gearfourth_role)
    # Log : Rôle ajouté
    print(f"[LOG] {ctx.author} a reçu le rôle Gear Fourth.")

    # Mettre à jour le cooldown
    collection47.update_one({"user_id": ctx.author.id}, {"$set": {"last_used": datetime.datetime.utcnow()}}, upsert=True)
    
    # Retirer le rôle après 1 jour
    await ctx.send(f"Félicitations {ctx.author.mention}, tu as activé le Gear Fourth ! Le rôle sera retiré dans 24 heures.")
    # Log : Notification de succès
    print(f"[LOG] {ctx.author} a activé Gear Fourth, rôle retiré dans 24 heures.")

    # Délai de 1 jour pour retirer le rôle
    await asyncio.sleep(86400)  # 86400 secondes = 1 jour
    await ctx.author.remove_roles(gearfourth_role)
    # Log : Rôle retiré après 24h
    print(f"[LOG] {ctx.author} a perdu le rôle Gear Fourth après 24 heures.")

    await ctx.send(f"{ctx.author.mention}, ton rôle Gear Fourth a été retiré après 24 heures.")

    # Image de l'embed
    embed = discord.Embed(
        title="Gear Fourth Activated!",
        description="Tu as activé la transformation Gear Fourth, tu deviens plus puissant pendant 1 jour !",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_image(url="https://pm1.aminoapps.com/7268/e216da33726458f8e0600f4affbd934465ea7c72r1-750-500v2_uhq.jpg")
    await ctx.send(embed=embed)
    # Log : Embed envoyé
    print(f"[LOG] {ctx.author} a reçu l'embed de confirmation Gear Fourth.")

#------------------------------------------------------------ Nika Nika no Mi
# Commande .nika
@bot.command()
async def nika(ctx):
    user = ctx.author
    role_id = 1365313292477927464  # Le rôle nécessaire pour utiliser la commande

    # Vérification du rôle de l'utilisateur
    if not any(role.id == role_id for role in user.roles):
        await ctx.send("Désolé, vous n'avez pas le rôle requis pour utiliser cette commande.")
        print(f"[LOG] {user} n'a pas le rôle requis pour utiliser la commande nika.")
        return

    # Vérification du cooldown
    cooldown_data = collection49.find_one({"user_id": user.id})
    if cooldown_data:
        last_used = cooldown_data["last_used"]
        cooldown_end = last_used + timedelta(weeks=2)
        if datetime.utcnow() < cooldown_end:
            await ctx.send(f"Vous devez attendre encore {cooldown_end - datetime.utcnow()} avant de réutiliser la commande.")
            print(f"[LOG] {user} est en cooldown. Prochain usage autorisé à {cooldown_end}.")
            return

    # Appliquer le rôle
    new_role = discord.utils.get(ctx.guild.roles, id=1365313243580469359)  # Rôle à attribuer
    if new_role:
        await user.add_roles(new_role)
        await ctx.send(f"{user.mention}, vous avez reçu le rôle {new_role.name} pendant 1 semaine.")
        print(f"[LOG] {user} a reçu le rôle {new_role.name} pendant 1 semaine.")

        # Retirer le rôle après 1 semaine
        await asyncio.sleep(604800)  # Attendre 1 semaine (604800 secondes)
        await user.remove_roles(new_role)
        await ctx.send(f"{user.mention}, le rôle {new_role.name} a été retiré après 1 semaine.")
        print(f"[LOG] {user} a perdu le rôle {new_role.name} après 1 semaine.")

    # Enregistrer le cooldown
    collection49.update_one(
        {"user_id": user.id},
        {"$set": {"last_used": datetime.utcnow()}},
        upsert=True
    )
    print(f"[LOG] Cooldown enregistré pour {user}. Prochaine utilisation possible : {datetime.utcnow()}.")

    # Ajouter l'image à l'embed
    embed = discord.Embed(
        title="Royaume de Nika activé!",
        description="Vous avez activé le pouvoir du Hito Hito no Mi - modèle Nika.",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.set_image(url="https://onepiecetheorie.fr/wp-content/uploads/2022/03/Hito-Hito-no-Mi-modele-Nika.jpg")
    
    await ctx.send(embed=embed)
    print(f"[LOG] L'embed pour le pouvoir Nika a été envoyé à {user}.")

# Configuration des logs
logging.basicConfig(level=logging.INFO)

@bot.command()
async def eveil(ctx):
    user_id = ctx.author.id
    role_required = 1365311605457555506
    role_temporaire = 1365312301900501063
    cooldown_duration = 30 * 24 * 60 * 60  # 1 mois

    # Vérifier si l'utilisateur a le rôle nécessaire
    if role_required not in [role.id for role in ctx.author.roles]:
        logging.warning(f"Utilisateur {ctx.author.name} ({ctx.author.id}) a tenté d'utiliser la commande /eveil sans avoir le rôle requis.")
        return await ctx.send("❌ Tu n'as pas le rôle nécessaire pour utiliser cette commande.")

    logging.info(f"Utilisateur {ctx.author.name} ({ctx.author.id}) a le rôle nécessaire pour utiliser la commande /eveil.")

    now = datetime.datetime.utcnow()
    cooldown_data = cd_eveil.find_one({"_id": user_id})

    if cooldown_data:
        cooldown_time = cooldown_data["cooldown"]
        if now < cooldown_time:
            remaining = cooldown_time - now
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            logging.info(f"Utilisateur {ctx.author.name} ({ctx.author.id}) a essayé d'utiliser /eveil avant la fin du cooldown.")
            return await ctx.send(
                f"⏳ Tu dois attendre encore **{hours}h {minutes}m {seconds}s** avant de pouvoir utiliser cette commande à nouveau."
            )

    # Appliquer le rôle temporaire
    role = ctx.guild.get_role(role_temporaire)
    await ctx.author.add_roles(role)

    logging.info(f"Rôle d'éveil attribué à {ctx.author.name} ({ctx.author.id}).")

    embed = discord.Embed(
        title="🌟 Éveil Activé !",
        description=f"{ctx.author.mention} entre dans un état d'éveil absolu !",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Durée : 20 secondes", icon_url=ctx.author.display_avatar.url)
    embed.set_image(url="https://www.melty.fr/wp-content/uploads/meltyfr/2022/08/one-piece-capitulo-1045-poderes-luffy.jpg")
    await ctx.send(embed=embed)

    # Mettre à jour le cooldown
    cd_eveil.update_one(
        {"_id": user_id},
        {"$set": {"cooldown": now + datetime.timedelta(seconds=cooldown_duration)}},
        upsert=True
    )

    logging.info(f"Cooldown mis à jour pour {ctx.author.name} ({ctx.author.id}).")

    # Attente et retrait du rôle
    await asyncio.sleep(20)
    await ctx.author.remove_roles(role)

    logging.info(f"Rôle d'éveil retiré de {ctx.author.name} ({ctx.author.id}).")

    embed_fin = discord.Embed(
        title="🌌 Fin de l'Éveil",
        description=f"L'état éveillé de {ctx.author.mention} s'est dissipé...",
        color=discord.Color.dark_blue()
    )
    await ctx.send(embed=embed_fin)

@bot.command(name="eveil2")
@commands.has_role(1365311605457555506)
async def eveil2(ctx, member: discord.Member):
    author_id = ctx.author.id
    now = datetime.utcnow()

    # Vérification du cooldown
    cooldown_data = collection_cd_eveil2.find_one({"user_id": author_id})
    if cooldown_data:
        last_used = cooldown_data["last_used"]
        cooldown_expiry = last_used + timedelta(weeks=5)  # 1 mois + 1 semaine
        if now < cooldown_expiry:
            remaining = cooldown_expiry - now
            days = remaining.days
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60

            embed_cd = discord.Embed(
                title="⛔ Cooldown actif",
                description=f"Tu dois encore attendre **{days} jours, {hours} heures et {minutes} minutes** avant de réutiliser cette commande.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed_cd)
            return

    # Vérification du rôle
    if not any(role.id == 1365311605457555506 for role in ctx.author.roles):
        print(f"[{now}] {ctx.author} n'a pas le rôle requis pour utiliser `.eveil2`.")
        await ctx.send("⛔ Tu n’as pas le rôle requis pour utiliser cette commande.")
        return

    # Application du rôle
    role = ctx.guild.get_role(1365313255471579297)
    if not role:
        print(f"[{now}] Le rôle {1365313255471579297} est introuvable.")
        return await ctx.send("❌ Le rôle à donner est introuvable.")

    await member.add_roles(role)

    embed = discord.Embed(
        title="🌟 Éveil Transcendantal",
        description=f"{ctx.author.mention} a accordé à {member.mention} un **pouvoir éveillé** pour **7 jours**.",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Un pouvoir rare accordé pour une durée limitée.", icon_url=member.display_avatar.url)
    embed.set_image(url="https://staticg.sportskeeda.com/editor/2023/08/d9dc7-16914260703952-1920.jpg")
    await ctx.send(embed=embed)

    # Enregistrement du cooldown
    collection_cd_eveil2.update_one(
        {"user_id": author_id},
        {"$set": {"last_used": now}},
        upsert=True
    )

    # Supprimer le rôle après 7 jours
    await asyncio.sleep(7 * 24 * 60 * 60)  # 7 jours
    try:
        await member.remove_roles(role)
        embed_fin = discord.Embed(
            title="⏳ Pouvoir dissipé",
            description=f"Le pouvoir éveillé de {member.mention} a disparu...",
            color=discord.Color.dark_blue()
        )
        await ctx.send(embed=embed_fin)
    except Exception as e:
        print(f"Erreur en retirant le rôle : {e}")

# Gestion des erreurs d'accès
@eveil2.error
async def eveil2_error(ctx, error):
    now = datetime.utcnow()
    if isinstance(error, commands.MissingRole):
        print(f"[{now}] {ctx.author} n’a pas le rôle requis pour utiliser `.eveil2`.")
        await ctx.send("⛔ Tu n’as pas le rôle requis pour utiliser cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"[{now}] Mauvaise utilisation de la commande `.eveil2` par {ctx.author}.")
        await ctx.send("❗ Utilisation : `.eveil2 @membre`")
    else:
        print(f"[{now}] Une erreur inconnue est survenue pour {ctx.author}.")
        await ctx.send("❌ Une erreur est survenue.")
        raise error
#---------------------------------------------------- Uo Uo no Mi, Modèle : Seiryu (Dragon Céleste)
@bot.command()
@commands.guild_only()
async def bourrasque(ctx, member: discord.Member = None):
    # Vérifie si l'utilisateur a le bon rôle
    if not any(role.id == 1365312299090313216 for role in ctx.author.roles):
        await ctx.send("❌ Tu n'as pas le pouvoir d'utiliser cette commande.")
        # Log de l'utilisateur sans le rôle
        print(f"[LOG] {ctx.author.name} ({ctx.author.id}) a essayé d'utiliser la commande bourrasque sans avoir le rôle nécessaire.")
        return

    # Vérifie si la cible est spécifiée
    if not member:
        await ctx.send("❌ Aucune cible spécifiée.")
        # Log de l'absence de cible
        print(f"[LOG] {ctx.author.name} ({ctx.author.id}) a essayé d'utiliser la commande bourrasque sans spécifier de cible.")
        return

    user_id = ctx.author.id
    target_id = member.id
    now = datetime.utcnow()

    # Vérification du cooldown (1 mois + 1 semaine)
    cooldown_data = collection53.find_one({"user_id": user_id})
    if cooldown_data:
        last_used = cooldown_data.get("last_used")
        if last_used and now < last_used + timedelta(weeks=5):
            remaining = (last_used + timedelta(weeks=5)) - now
            days = remaining.days
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            embed_cd = discord.Embed(
                title="⏳ Cooldown actif",
                description=f"Tu dois attendre encore **{days} jours, {hours} heures et {minutes} minutes** avant de réutiliser cette commande.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed_cd)
            # Log du cooldown actif
            print(f"[LOG] {ctx.author.name} ({ctx.author.id}) a essayé d'utiliser bourrasque avant la fin du cooldown.")
            return

    # Donner le rôle à la cible
    role = ctx.guild.get_role(1365235019869847572)
    if not role:
        await ctx.send("❌ Le rôle cible est introuvable.")
        # Log de rôle introuvable
        print(f"[LOG] Le rôle cible pour la commande bourrasque est introuvable dans le serveur.")
        return

    try:
        await member.add_roles(role)
    except discord.DiscordException as e:
        await ctx.send(f"❌ Une erreur est survenue en attribuant le rôle à {member.mention}.")
        # Log d'erreur lors de l'ajout de rôle
        print(f"[LOG] Erreur en attribuant le rôle bourrasque à {member.name} ({member.id}): {str(e)}")
        return

    embed = discord.Embed(
        title="🌪️ Bourrasque Déchaînée !",
        description=f"{ctx.author.mention} a invoqué une **bourrasque puissante** sur {member.mention} !\n"
                    f"Le rôle est actif pour **24 heures**.",
        color=discord.Color.teal()
    )
    embed.set_image(url="https://static.wikia.nocookie.net/onepiece/images/4/4d/Boro_Breath.png/revision/latest?cb=20210207230101&path-prefix=fr")
    embed.set_footer(text="Un vent divin balaie tout sur son passage...", icon_url=member.display_avatar.url)
    await ctx.send(embed=embed)

    # Stocker le cooldown dans MongoDB
    collection53.update_one(
        {"user_id": user_id},
        {"$set": {"last_used": now}},
        upsert=True
    )

    # Stocker la fin de l’effet dans une autre collection
    collection54.update_one(
        {"user_id": target_id},
        {
            "$set": {
                "end_time": now + timedelta(days=1),
                "role_id": 1365235019869847572,
                "guild_id": ctx.guild.id
            }
        },
        upsert=True
    )

    # Log de la commande réussie
    print(f"[LOG] {ctx.author.name} ({ctx.author.id}) a utilisé la commande bourrasque sur {member.name} ({member.id}).")

@bot.command()
async def tonnerre(ctx, member: discord.Member = None):
    role_required = 1365311614332571739
    role_to_give = 1365312292069048443
    cooldown_collection = collection56  # cd_tonnerre_attaque

    # Vérification de la présence de la cible
    if member is None:
        print(f"[LOG] {ctx.author} n'a pas mentionné de membre pour la commande tonnerre.")
        return await ctx.send("❌ Tu dois mentionner un membre pour utiliser la commande.")

    # Vérification du rôle de l'utilisateur
    if role_required not in [r.id for r in ctx.author.roles]:
        print(f"[LOG] {ctx.author} a tenté d'utiliser la commande tonnerre sans le rôle requis.")
        return await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande ⚡.")

    now = datetime.utcnow()
    user_cooldown = cooldown_collection.find_one({"user_id": ctx.author.id})

    # Vérification du cooldown
    if user_cooldown and (now - user_cooldown["last_use"]).days < 30:
        remaining = 30 - (now - user_cooldown["last_use"]).days
        embed_cd = discord.Embed(
            title="⏳ Cooldown actif",
            description=f"Tu dois encore attendre **{remaining} jours** avant de pouvoir invoquer la foudre à nouveau.",
            color=discord.Color.red()
        )
        print(f"[LOG] {ctx.author} a tenté d'utiliser la commande tonnerre, mais est encore en cooldown de {remaining} jours.")
        await ctx.send(embed=embed_cd)
        return

    # Vérification du rôle à attribuer
    role = ctx.guild.get_role(role_to_give)
    if not role:
        print(f"[LOG] Rôle introuvable: {role_to_give}")
        return await ctx.send("❌ Le rôle à attribuer est introuvable.")

    # Appliquer le rôle
    try:
        await member.add_roles(role)
        print(f"[LOG] {ctx.author} a donné le rôle {role.name} à {member}.")
    except Exception as e:
        print(f"[LOG] Erreur lors de l'ajout du rôle à {member}: {e}")
        return await ctx.send(f"❌ Une erreur s'est produite en essayant d'ajouter le rôle à {member.mention}.")

    embed = discord.Embed(
        title="⚡ Tonnerre Divin !",
        description=f"{ctx.author.mention} a libéré un **éclair dévastateur** sur {member.mention} !\n"
                    f"Le pouvoir du tonnerre sera actif pendant **2 semaines**.",
        color=discord.Color.dark_purple()
    )
    embed.set_image(url="https://www.japanfm.fr/wp-content/uploads/2024/03/one-piece-kaido-scaled.jpg")
    embed.set_footer(text="Un grondement retentit dans les cieux...", icon_url=member.display_avatar.url)
    await ctx.send(embed=embed)

    # Mise à jour du cooldown
    try:
        cooldown_collection.update_one(
            {"user_id": ctx.author.id},
            {"$set": {"last_use": now}},
            upsert=True
        )
        print(f"[LOG] {ctx.author} a mis à jour son cooldown.")
    except Exception as e:
        print(f"[LOG] Erreur lors de la mise à jour du cooldown de {ctx.author}: {e}")
        return await ctx.send("❌ Une erreur s'est produite en essayant de mettre à jour le cooldown.")

    # Planification du retrait après 2 semaines
    async def remove_role_later():
        await asyncio.sleep(14 * 24 * 60 * 60)  # 14 jours
        if role in member.roles:
            try:
                await member.remove_roles(role)
                print(f"[LOG] {role.name} retiré de {member}.")
                end_embed = discord.Embed(
                    title="⚡ Fin du Jugement",
                    description=f"Le **tonnerre** s'est dissipé. {member.mention} est désormais libéré de son pouvoir électrique.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=end_embed)
            except Exception as e:
                print(f"[LOG] Erreur lors du retrait du rôle de {member}: {e}")

    bot.loop.create_task(remove_role_later())

@bot.command()
@commands.has_role(1365311614332571739)
async def dragon(ctx, user: discord.Member = None):
    # Vérifie si l'utilisateur a le rôle nécessaire
    if not any(role.id == 1365311614332571739 for role in ctx.author.roles):
        log_message = f"[{datetime.utcnow()}] {ctx.author} a tenté d'utiliser la commande dragon sans le rôle requis."
        print(log_message)  # Log en console
        await ctx.send("Désolé, tu n'as pas le rôle nécessaire pour utiliser cette commande.")
        return

    # Vérifie si une cible est spécifiée
    if not user:
        log_message = f"[{datetime.utcnow()}] {ctx.author} a tenté d'utiliser la commande dragon sans cible."
        print(log_message)  # Log en console
        await ctx.send("Tu dois spécifier un utilisateur à cibler.")
        return

    # Vérifie si l'utilisateur a déjà utilisé la commande
    cd_data = collection58.find_one({"user_id": user.id})
    
    if cd_data:
        cooldown_end = cd_data.get("cooldown_end")
        if cooldown_end and datetime.utcnow() < cooldown_end:
            remaining_time = cooldown_end - datetime.utcnow()
            embed_cd = discord.Embed(
                title="⏳ Cooldown Actif",
                description=f"Tu dois attendre encore **{remaining_time}** avant de pouvoir invoquer la puissance du dragon à nouveau.",
                color=discord.Color.red()
            )
            log_message = f"[{datetime.utcnow()}] {ctx.author} a tenté d'utiliser la commande dragon sur {user}, mais un cooldown est actif."
            print(log_message)  # Log en console
            await ctx.send(embed=embed_cd)
            return

    # Log lorsque l'utilisateur est ciblé
    log_message = f"[{datetime.utcnow()}] {ctx.author} a invoqué la puissance du dragon sur {user}."
    print(log_message)  # Log en console

    # Réduire le total de la personne ciblée à 0
    collection.update_one(
        {"user_id": user.id},
        {"$set": {"balance": 0, "bank": 0}},
        upsert=True
    )
    
    # Log de la réduction des coins
    log_message = f"[{datetime.utcnow()}] {user} a vu son total réduit à zéro par la puissance du dragon."
    print(log_message)  # Log en console

    # Ajoute un cooldown d'un mois
    cooldown_end = datetime.utcnow() + timedelta(days=30)
    collection58.update_one(
        {"user_id": user.id},
        {"$set": {"cooldown_end": cooldown_end}},
        upsert=True
    )
    
    # Log de l'ajout du cooldown
    log_message = f"[{datetime.utcnow()}] Un cooldown d'un mois a été ajouté pour {user}."
    print(log_message)  # Log en console

    # Préparer l'embed avec l'image de Kaido
    embed = discord.Embed(
        title="🐉 La Puissance du Dragon !",
        description=f"{user.mention} a été frappé par la **force du dragon** ! Leur total a été réduit à zéro par la colère divine de Kaido.\n"
                    f"Un **mois** de cooldown est désormais imposé à {user.mention} avant de pouvoir réagir.",
        color=discord.Color.orange()
    )
    embed.set_image(url="https://www.japanfm.fr/wp-content/uploads/2024/03/one-piece-kaido-scaled.jpg")
    embed.set_footer(text="Le dragon règne sur la mer... et son pouvoir est irrésistible.", icon_url=user.display_avatar.url)
    
    # Envoi de l'embed
    await ctx.send(embed=embed)

@bot.command(name="suicide")
async def suicide(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")

    authorized_roles = [
        1365316070172393572, 1365311588139274354, 1365313257279062067,
        1365311602290851880, 1365313248269828116, 1365311608259346462,
        1365313251201519697, 1365311611019202744, 1365311614332571739,
        1365313292477927464
    ]

    # Vérifie si l'utilisateur a un des rôles autorisés
    if not any(role.id in authorized_roles for role in ctx.author.roles):
        return await ctx.send("❌ Tu n'as pas le droit d'utiliser cette commande.")

    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Récupération ou création de la data utilisateur
    def get_or_create_user_data(guild_id: int, user_id: int):
        data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
        if not data:
            data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
            collection.insert_one(data)
        return data

    data = get_or_create_user_data(guild_id, user_id)
    cash = data.get("cash", 0)
    bank = data.get("bank", 0)
    total = cash + bank

    # Calcul de 5% du total
    five_percent = int(total * 0.05)

    # Retrait de 5% en priorité du cash, puis de la banque
    if cash >= five_percent:
        new_cash = cash - five_percent
        new_bank = bank
    else:
        remaining = five_percent - cash
        new_cash = 0
        new_bank = max(bank - remaining, 0)

    # Mise à jour de la base de données
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"cash": new_cash, "bank": new_bank}}
    )

    # Suppression des rôles
    roles_to_remove = [ctx.guild.get_role(role_id) for role_id in authorized_roles]
    await ctx.author.remove_roles(*filter(None, roles_to_remove), reason="Suicide RP - Retrait de fruit")

    # Création de l'embed
    embed = discord.Embed(
        title="☠️ Suicide ☠️",
        description=(
            "Dans un dernier souffle, tu abandonnes ton pouvoir... ton fruit est désormais perdu, "
            "et ton âme erre sans force sur les mers de ce monde cruel.\n\n"
            "En te libérant, tu as également sacrifié **5%** de ta richesse."
        ),
        color=discord.Color.dark_purple()
    )
    embed.set_image(url="https://www.melty.fr/wp-content/uploads/meltyfr/2022/01/media-2796-736x414.jpg")
    embed.set_footer(text="Ton sacrifice sera peut-être honoré... ou vite oublié.")

    await ctx.send(embed=embed)

@bot.command(name="rayleigh")
async def rayleigh(ctx):
    if ctx.guild is None:
        return await ctx.send("Cette commande doit être utilisée dans un serveur.")

    armement_v1 = 1365698043684327424
    observation_v1 = 1365698125754404975
    armement_v2 = 1365699319163785246
    observation_v2 = 1365699245377847448

    required_roles = [armement_v1, observation_v1]

    # Vérifie que l'auteur a un des deux rôles
    if not any(role.id in required_roles for role in ctx.author.roles):
        return await ctx.send("Tu n'as pas le rôle requis pour utiliser cette commande.")

    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Fonction pour récupérer ou créer la donnée utilisateur
    def get_or_create_user_data(guild_id: int, user_id: int):
        data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
        if not data:
            data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
            collection.insert_one(data)
        return data

    data = get_or_create_user_data(guild_id, user_id)
    cash = data.get("cash", 0)

    if cash < 100000:
        return await ctx.send("Tu n'as pas assez de cash pour apprendre une maîtrise avancée ! (100,000 requis)")

    # Déduction des 100,000 cash
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -100000}}
    )

    embed = discord.Embed(color=discord.Color.gold())
    embed.set_author(name="Maître Rayleigh", icon_url="https://static.wikia.nocookie.net/onepiece/images/3/37/Silvers_Rayleigh_Anime_Pre_Timeskip_Infobox.png")

    # Donne le bon rôle selon celui de base
    if any(role.id == armement_v1 for role in ctx.author.roles):
        role = ctx.guild.get_role(armement_v2)
        await ctx.author.add_roles(role)

        embed.title = "Haki de l'Armement Avancé !"
        embed.description = (
            f"**{ctx.author.mention}**, grâce à ton entraînement rigoureux avec Rayleigh, "
            "tu as débloqué la **version avancée du Haki de l'Armement** ! 💥\n\n"
            "Ton corps est maintenant capable d'infuser ton Haki de manière offensive. Prépare-toi à écraser tes ennemis !"
        )
        embed.set_image(url="https://fictionhorizon.com/wp-content/uploads/2023/03/LuffySilvers.jpg")

    elif any(role.id == observation_v1 for role in ctx.author.roles):
        role = ctx.guild.get_role(observation_v2)
        await ctx.author.add_roles(role)

        embed.title = "Haki de l'Observation Avancé !"
        embed.description = (
            f"**{ctx.author.mention}**, ton entraînement acharné avec Rayleigh t'a permis de débloquer "
            "**le Haki de l'Observation avancé** ! 👁️\n\n"
            "Tu peux désormais prédire les mouvements de tes ennemis avec une précision inégalée."
        )
        embed.set_image(url="https://preview.redd.it/a9vxdbetg1pd1.jpeg?auto=webp&s=74386433a136b3c31375ff21a5209c9f2dc26a74")

    else:
        return await ctx.send("Erreur : aucun rôle de V1 détecté.")

    await ctx.send(embed=embed)

@bot.command()
async def wobservation(ctx):
    role_required = 1365389687618928885  # ID du rôle qui peut utiliser la commande
    role_to_give = 1365720903475925102   # ID du rôle à donner
    cooldown_duration = 14 * 24 * 60 * 60  # 2 semaines en secondes

    # Vérifie si l'auteur a le bon rôle
    if role_required not in [role.id for role in ctx.author.roles]:
        return await ctx.send("🚫 Tu n'as pas le rôle requis pour utiliser cette commande.")

    # Vérifie le cooldown
    cooldown_data = collection60.find_one({"user_id": ctx.author.id})
    now = datetime.utcnow()

    if cooldown_data:
        cooldown_end = cooldown_data.get("cooldown_end")
        if cooldown_end and now < cooldown_end:
            remaining = cooldown_end - now
            minutes, seconds = divmod(remaining.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            return await ctx.send(f"⏳ Tu dois encore attendre **{int(days)}j {int(hours)}h {int(minutes)}m** avant de pouvoir réutiliser cette commande.")

    # Donne le rôle
    role = ctx.guild.get_role(role_to_give)
    if role is None:
        return await ctx.send("❌ Le rôle à donner est introuvable.")

    await ctx.author.add_roles(role)
    await ctx.send(f"✅ {ctx.author.mention} a reçu le rôle {role.mention} pour 1 minute !")

    # Définir le cooldown dans Mongo
    collection60.update_one(
        {"user_id": ctx.author.id},
        {"$set": {"cooldown_end": now + timedelta(seconds=cooldown_duration)}},
        upsert=True
    )

    # Attend 1 minute
    await asyncio.sleep(60)

    # Retirer le rôle
    await ctx.author.remove_roles(role)
    try:
        await ctx.author.send("⏳ Ton rôle d'observation vient d'expirer.")
    except discord.Forbidden:
        pass  # DM bloqué, on ignore

# Ton rôle nécessaire renommé ici
OBSERVATION_ID = 1365698125754404975

# Le rôle à donner temporairement
TEMP_ROLE_ID = 1365724876689768498

# Cooldown en secondes (1 semaine)
COOLDOWN_SECONDS = 7 * 24 * 60 * 60  # 604800 secondes

@bot.command(name="observation")
async def observation(ctx):
    if not any(role.id == OBSERVATION_ID for role in ctx.author.roles):
        return await ctx.send("❌ Tu n'as pas le rôle nécessaire pour utiliser cette commande.")

    cooldown_data = collection61.find_one({"user_id": ctx.author.id})
    now = datetime.utcnow()

    if cooldown_data and cooldown_data.get("next_use") and cooldown_data["next_use"] > now:
        remaining = cooldown_data["next_use"] - now
        heures, secondes = divmod(remaining.total_seconds(), 3600)
        minutes, secondes = divmod(secondes, 60)
        return await ctx.send(f"⏳ Tu pourras réutiliser cette commande dans {int(heures)}h {int(minutes)}m {int(secondes)}s.")

    role = ctx.guild.get_role(TEMP_ROLE_ID)
    if not role:
        return await ctx.send("❌ Rôle temporaire introuvable.")

    try:
        await ctx.author.add_roles(role)
        await ctx.send(f"🌀 **Observation activée !** Le rôle te sera retiré dans 10 secondes...")
        
        await asyncio.sleep(10)

        await ctx.author.remove_roles(role)
        await ctx.send("🔚 **Observation terminée !** Le rôle a été retiré.")
        
        next_use_time = now + timedelta(seconds=COOLDOWN_SECONDS)
        collection61.update_one(
            {"user_id": ctx.author.id},
            {"$set": {"next_use": next_use_time}},
            upsert=True
        )

    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas la permission de gérer les rôles.")
    except Exception as e:
        await ctx.send(f"❌ Une erreur est survenue: {e}")

NEUTRAL_ROLE_ID = 1365728799832150096
PIRATE_ROLE_ID = 1365682636957421741
MARINE_ROLE_ID = 1365631932964012142

class ChooseCamp(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=None)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Bloque les autres utilisateurs
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Tu ne peux pas utiliser ce menu.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Pirate", style=ButtonStyle.danger)
    async def pirate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        if discord.utils.get(member.roles, id=NEUTRAL_ROLE_ID) is None:
            await interaction.response.send_message("Tu n'as pas accès à ce choix.", ephemeral=True)
            return
        
        pirate_role = member.guild.get_role(PIRATE_ROLE_ID)
        neutral_role = member.guild.get_role(NEUTRAL_ROLE_ID)

        await member.add_roles(pirate_role)
        await member.remove_roles(neutral_role)

        await interaction.message.delete()  # <- Supprime le message avec les boutons
        await interaction.response.send_message("Tu as choisi le camp **Pirate** ! 🏴‍☠️", ephemeral=True)

    @discord.ui.button(label="Marine", style=ButtonStyle.primary)
    async def marine_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        if discord.utils.get(member.roles, id=NEUTRAL_ROLE_ID) is None:
            await interaction.response.send_message("Tu n'as pas accès à ce choix.", ephemeral=True)
            return
        
        marine_role = member.guild.get_role(MARINE_ROLE_ID)
        neutral_role = member.guild.get_role(NEUTRAL_ROLE_ID)

        await member.add_roles(marine_role)
        await member.remove_roles(neutral_role)

        await interaction.message.delete()  # <- Supprime le message avec les boutons
        await interaction.response.send_message("Tu as choisi le camp **Marine** ! ⚓", ephemeral=True)

@bot.command()
async def neutre(ctx):
    # Vérifie si la personne a le rôle neutre
    if discord.utils.get(ctx.author.roles, id=NEUTRAL_ROLE_ID) is None:
        await ctx.send("Tu n'as pas accès à cette commande.")
        return

    embed = discord.Embed(
        title="Choisis ton camp !",
        description=(
            "Il est temps de choisir ta voie...\n"
            "**Pirate** 🏴‍☠️ ou **Marine** ⚓ ?\n\n"
            "Une fois ton choix fait, tu ne pourras pas revenir en arrière facilement !"
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdJ8fqMr7UyPIQ5K2lnTKaEcdVktMal6pxaQ&s")

    await ctx.send(embed=embed, view=ChooseCamp(ctx.author.id))

PING_ROLE_ID = 1355190216188497951

@bot.command(name="divin")
async def divin(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("Tu n'as pas la permission d'utiliser cette commande.")

    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Données MongoDB
    data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not data:
        data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection.insert_one(data)

    # Ajout des 500 000 à la banque
    new_bank = data.get("bank", 0) + 500_000
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"bank": new_bank}}
    )

    # Attribution du rôle divin
    role = ctx.guild.get_role(DIVIN_ROLE_ID)
    if role:
        await ctx.author.add_roles(role)

    # Ping du rôle juste avant
    await ctx.send(f"<@&{PING_ROLE_ID}>")

    # Embed ZINZIN
    embed = discord.Embed(
        title="🌌 L'ŒIL DIVIN D'ETHER S'EST OUVERT 🌌",
        description=(
            f"⚠️ **Instabilité cosmique détectée...**\n\n"
            f"Une énergie ancestrale vient de traverser les dimensions.\n\n"
            f"**{ctx.author.mention}** a été **choisi par l’Œil Divin d’Ether**, une relique d’un autre monde.\n\n"
            f"Son corps vibre d’un pouvoir **unique et inconnu**.\n"
            f"**+500,000** <:ecoEther:1341862366249357374> ont été déposés dans sa banque.\n"
            f"Le rôle <@&{DIVIN_ROLE_ID}> lui est désormais lié à jamais."
        ),
        color=discord.Color.purple()
    )
    embed.set_image(url="https://github.com/Iseyg91/Jeux_Eco/blob/main/76b1909809e2fcb7caa7f9cfa3e222c5.png?raw=true")
    embed.set_footer(text="⚡ Un nouvel équilibre vient de naître… ou de s'effondrer.")

    await ctx.send(embed=embed)
#------------------------------------------------- Gcreate
@bot.command(name="gcreate")
async def creer_guilde(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier s'il est déjà dans une guilde
    guilde_existante = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if guilde_existante:
        return await ctx.send("Tu es déjà dans une guilde.")

    # Vérifier les coins
    user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data or user_data.get("cash", 0) < 5000:
        return await ctx.send("Tu n'as pas assez de coins pour créer une guilde (5000 requis).")

    def check_msg(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Demander le nom de la guilde
    await ctx.send("📝 Quel est le nom de ta guilde ? (Ce sera l'ID interne)")
    try:
        msg_nom = await bot.wait_for("message", check=check_msg, timeout=60)
        nom_guilde = msg_nom.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Vérifier si une guilde avec ce nom existe déjà
    if collection35.find_one({"guild_id": guild_id, "guild_name": nom_guilde}):
        return await ctx.send("❌ Une guilde avec ce nom existe déjà.")

    # Demander la description
    await ctx.send("📄 Donne une petite description pour ta guilde :")
    try:
        msg_desc = await bot.wait_for("message", check=check_msg, timeout=60)
        description = msg_desc.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Demander une PFP pour la guilde
    await ctx.send("🎨 Envoie une image pour la photo de profil de ta guilde (PFP) :")
    try:
        msg_pfp = await bot.wait_for("message", check=check_msg, timeout=60)
        if not msg_pfp.attachments:
            return await ctx.send("❌ Tu n'as pas envoyé d'image pour la PFP.")
        pfp_url = msg_pfp.attachments[0].url
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Demander une bannière pour la guilde
    await ctx.send("🎨 Envoie une image pour la bannière de ta guilde :")
    try:
        msg_banniere = await bot.wait_for("message", check=check_msg, timeout=60)
        if not msg_banniere.attachments:
            return await ctx.send("❌ Tu n'as pas envoyé d'image pour la bannière.")
        banniere_url = msg_banniere.attachments[0].url
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Déduire les coins
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -5000}}
    )

    # Enregistrement dans la DB
    nouvelle_guilde = {
        "guild_id": guild_id,
        "guild_name": nom_guilde,
        "description": description,
        "pfp_url": pfp_url,
        "banniere_url": banniere_url,
        "bank": 0,
        "vault": 0,
        "membres": [
            {
                "user_id": user_id,
                "role": "Créateur",
                "joined_at": datetime.utcnow()
            }
        ]
    }

    collection35.insert_one(nouvelle_guilde)

    await ctx.send(f"✅ Guilde **{nom_guilde}** créée avec succès !")

@bot.command(name="ginvite")
async def ginvite(ctx, member: discord.Member):
    # Récupérer les informations de la guilde du joueur qui invite
    guild_id = ctx.guild.id
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde:
        return await ctx.send("Aucune guilde trouvée.")

    # Vérifier que l'auteur est bien le créateur
    createur = next((membre for membre in guilde["membres"] if membre["user_id"] == ctx.author.id and membre["role"] == "Créateur"), None)
    if not createur and ctx.author.id != guilde["membres"][0]["user_id"]:
        return await ctx.send("❌ Seul le créateur de la guilde peut inviter des membres.")

    guild_name = guilde.get("guild_name", "Inconnue")
    description = guilde.get("description", "Aucune description.")
    pfp_url = guilde.get("pfp_url")
    
    # Créer l'embed d'invitation
    embed = discord.Embed(
        title=f"Invitation à la guilde {guild_name}",
        description=f"Tu as été invité à rejoindre la guilde **{guild_name}** !\n\n{description}",
        color=discord.Color.blue()
    )
    
    if pfp_url:
        embed.set_thumbnail(url=pfp_url)

    # Créer les boutons "Accepter" et "Refuser"
    class InviteButtons(View):
        def __init__(self, inviter, invited_member):
            super().__init__()
            self.inviter = inviter
            self.invited_member = invited_member

        @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)
        async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Action quand le membre accepte l'invitation
            if interaction.user == self.invited_member:
                # Ajouter le membre à la guilde
                collection35.update_one(
                    {"guild_id": guild_id},
                    {"$push": {"membres": {"user_id": self.invited_member.id, "role": "Membre"}}}
                )
                await interaction.response.send_message(f"{self.invited_member.mention} a accepté l'invitation à la guilde {guild_name} !", ephemeral=True)
                # Envoie un message dans la guilde (optionnel)
                await ctx.send(f"{self.invited_member.mention} a rejoint la guilde {guild_name}.")

        @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red)
        async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Action quand le membre refuse l'invitation
            if interaction.user == self.invited_member:
                await interaction.response.send_message(f"{self.invited_member.mention} a refusé l'invitation.", ephemeral=True)

    # Créer la vue pour les boutons
    view = InviteButtons(ctx.author, member)

    # Envoyer l'embed et ajouter la vue avec les boutons dans le salon d'origine
    await ctx.send(embed=embed, view=view)

    await ctx.send(f"Une invitation a été envoyée à {member.mention}.")

@bot.command(name="g")
async def afficher_guilde(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Récupérer la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await ctx.send("Tu n'es dans aucune guilde.")

    guild_name = guilde.get("guild_name", "Inconnue")
    description = guilde.get("description", "Aucune description.")
    banque = guilde.get("bank", 0)
    coffre_fort = guilde.get("vault", 0)
    membres = guilde.get("membres", [])
    pfp_url = guilde.get("pfp_url")
    banniere_url = guilde.get("banniere_url")

    embed = discord.Embed(
        title=f"Informations sur la guilde : {guild_name}",
        color=discord.Color.blue()
    )

    # Ajouter la PFP si elle existe
    if pfp_url:
        embed.set_thumbnail(url=pfp_url)

    # Ajouter la bannière si elle existe
    if banniere_url:
        embed.set_image(url=banniere_url)

    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="Banque", value=f"{int(banque):,} <:ecoEther:1341862366249357374>", inline=True)  # Retirer les décimales
    embed.add_field(name="Coffre fort", value=f"{int(coffre_fort):,} / 750,000 <:ecoEther:1341862366249357374>", inline=True)  # Retirer les décimales
    embed.add_field(name="ID", value=guilde.get("guild_name"), inline=False)

    # Affichage des membres
    membre_text = ""
    for membre in membres:
        mention = f"<@{membre['user_id']}>"
        role = membre.get("role", "Membre")
        if role == "Créateur":
            membre_text += f"**Créateur** | {mention}\n"
        else:
            membre_text += f"**Membre** | {mention}\n"

    embed.add_field(name=f"Membres ({len(membres)}/5)", value=membre_text or "Aucun membre", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="reset-teams")
async def reset_teams(ctx):
    # Vérifier si l'utilisateur a l'ID correct
    if ctx.author.id != 792755123587645461:
        return await ctx.send("Tu n'as pas la permission d'utiliser cette commande.")

    # Effacer toutes les guildes de la base de données
    result = collection35.delete_many({})
    
    if result.deleted_count > 0:
        await ctx.send(f"✅ Toutes les guildes ont été supprimées avec succès. {result.deleted_count} guildes supprimées.")
    else:
        await ctx.send("❌ Aucune guilde trouvée à supprimer.")

# Commande .cdep : Déposer des coins dans le coffre-fort de la guilde
@bot.command(name="cdep")
async def cdep(ctx, amount: int):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans une team
    user_team = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not user_team:
        return await ctx.send("❌ Tu n'es dans aucune team.")

    # Vérifier les coins de l'utilisateur
    user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data or user_data.get("cash", 0) < amount:
        return await ctx.send("❌ Tu n'as pas assez de coins pour faire ce dépôt.")

    # Déposer les coins dans le coffre-fort
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": user_id},  # Correction ici
        {"$inc": {"vault": amount}},
    )

    # Déduire les coins du joueur
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -amount}},
    )

    await ctx.send(f"✅ {int(amount):,} coins ont été déposés dans le coffre-fort de ta guilde.")

@bot.command(name="cwith")
async def cwith(ctx, amount: int):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans une team
    user_team = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not user_team:
        return await ctx.send("❌ Tu n'es dans aucune team.")

    # Récupérer les informations de la guilde
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde or guilde.get("vault", 0) < amount:
        return await ctx.send("❌ Le coffre-fort de la guilde n'a pas assez de coins.")

    # Retirer les coins du coffre-fort
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": user_id},  # Correction ici
        {"$inc": {"vault": -amount}},
    )
    
    # Ajouter les coins à la banque de la guilde
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": user_id},  # Correction ici aussi
        {"$inc": {"bank": amount}},
    )

    await ctx.send(f"✅ {int(amount):,} coins ont été retirés du coffre-fort de ta guilde.")

# Commande .gban : Bannir un membre de la guilde
@bot.command(name="gban")
async def gban(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si l'utilisateur est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas dans la guilde.")

    # Bannir le membre de la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id}}},
    )

    await ctx.send(f"{member.mention} a été banni de la guilde.")

@bot.command(name="gdelete")
async def gdelete(ctx, guild_id: int):
    # Vérifier que l'utilisateur est autorisé à supprimer la guilde (par exemple, propriétaire)
    if ctx.author.id != 792755123587645461:  # ISEY_ID
        return await ctx.send("Tu n'as pas la permission de supprimer cette guilde.")
    
    # Vérifier si la guilde existe dans la base de données
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde:
        return await ctx.send(f"Aucune guilde trouvée avec l'ID {guild_id}.")

    # Supprimer la guilde
    collection35.delete_one({"guild_id": guild_id})

    await ctx.send(f"La guilde avec l'ID {guild_id} a été supprimée avec succès.")

# Commande .gdep : Déposer des coins dans la banque de la guilde
@bot.command(name="gdep")
async def gdep(ctx, amount: str):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans une team
    user_team = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})  # Rechercher dans la sous-clé user_id de members
    if not user_team:
        return await ctx.send("❌ Tu n'es dans aucune team.")

    if amount == "all":
        # Déposer tout l'argent dans la banque
        user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
        amount = user_data.get("cash", 0)

        if amount == 0:
            return await ctx.send("❌ Tu n'as pas de coins à déposer.")

    # Convertir la quantité en entier
    try:
        amount = int(amount)
    except ValueError:
        return await ctx.send("❌ La quantité spécifiée n'est pas valide.")

    if amount <= 0:
        return await ctx.send("❌ Tu ne peux pas déposer une quantité de coins inférieure ou égale à 0.")

    # Vérifier que l'utilisateur a suffisamment de coins pour effectuer le dépôt
    user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if user_data.get("cash", 0) < amount:
        return await ctx.send("❌ Tu n'as pas assez de coins pour faire ce dépôt.")

    # Déposer les coins dans la banque de la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"bank": amount}},
    )

    # Déduire les coins du joueur
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -amount}},
    )

    await ctx.send(f"✅ {int(amount):,} coins ont été déposés dans la banque de ta guilde.")

# Commande .gkick : Expulser un membre de la guilde
@bot.command(name="gkick")
async def gkick(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si le membre est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas dans la guilde.")

    # Expulser le membre
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id}}},
    )

    await ctx.send(f"{member.mention} a été expulsé de la guilde.")

# Commande .gleave : Quitter la guilde
@bot.command(name="gleave")
async def gleave(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == user_id for membre in guilde['membres']):
        return await ctx.send("Tu n'es pas dans cette guilde.")

    # Quitter la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": user_id}}},
    )

    await ctx.send(f"{ctx.author.mention} a quitté la guilde.")

# Commande .gowner : Transférer la propriété de la guilde
@bot.command(name="gowner")
async def gowner(ctx, new_owner: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si l'utilisateur est le propriétaire actuel (par exemple, le créateur)
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == ctx.author.id and membre['role'] == 'Créateur' for membre in guilde['membres']):
        return await ctx.send("Tu n'es pas le propriétaire de la guilde.")

    # Transférer la propriété
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": ctx.author.id},
        {"$set": {"membres.$.role": "Membre"}},
    )
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": new_owner.id},
        {"$set": {"membres.$.role": "Créateur"}},
    )

    await ctx.send(f"La propriété de la guilde a été transférée à {new_owner.mention}.")

# Commande .gunban : Débannir un membre de la guilde
@bot.command(name="gunban")
async def gunban(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si le membre est banni
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id and membre['role'] == 'Banni' for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas banni de cette guilde.")

    # Débannir le membre
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id, "role": "Banni"}}},
    )

    await ctx.send(f"{member.mention} a été débanni de la guilde.")

# Commande .gwith : Retirer des coins de la banque de la guilde
@bot.command(name="gwith")
async def gwith(ctx, amount: int):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans une team
    user_team = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})  # Rechercher dans la sous-clé user_id de members
    if not user_team:
        return await ctx.send("❌ Tu n'es dans aucune team.")

    # Récupérer les informations de la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or guilde.get("bank", 0) < amount:
        return await ctx.send("❌ La banque de la guilde n'a pas assez de coins.")

    # Retirer les coins de la banque
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"bank": -amount}},
    )

    # Ajouter les coins au joueur (ici on les ajoute à l'auteur de la commande)
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": amount}},
    )

    await ctx.send(f"✅ {amount:,} coins ont été retirés de la banque de ta guilde.")

@bot.tree.command(name="dep-guild-inventory", description="Dépose un item de ton inventaire vers celui de ta guilde")
@app_commands.describe(item_id="ID de l'item à transférer", quantite="Quantité à transférer")
async def dep_guild_inventory(interaction: discord.Interaction, item_id: int, quantite: int):
    user = interaction.user
    guild_id = interaction.guild.id
    user_id = user.id

    if quantite <= 0:
        return await interaction.response.send_message("❌ La quantité doit être supérieure à 0.", ephemeral=True)

    # Vérifie la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await interaction.response.send_message("❌ Tu n'es dans aucune guilde.", ephemeral=True)

    # Vérifie l'inventaire du joueur
    items = list(collection17.find({
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": item_id
    }))

    if len(items) < quantite:
        return await interaction.response.send_message(f"❌ Tu n'as pas `{quantite}` de cet item dans ton inventaire.", ephemeral=True)

    # Supprimer les items du joueur
    for i in range(quantite):
        collection17.delete_one({
            "_id": items[i]["_id"]
        })

    # Ajouter à l'inventaire de la guilde
    existing = collection36.find_one({
        "guild_id": guild_id,
        "item_id": item_id
    })

    if existing:
        collection36.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": quantite}}
        )
    else:
        # On récupère les infos du premier item pour les détails
        item_data = items[0]
        collection36.insert_one({
            "guild_id": guild_id,
            "item_id": item_id,
            "item_name": item_data.get("item_name", "Inconnu"),
            "emoji": item_data.get("emoji", ""),
            "quantity": quantite
        })

    await interaction.response.send_message(
        f"✅ Tu as transféré **{quantite}x** `{item_id}` dans l'inventaire de ta guilde.",
        ephemeral=True
    )

@bot.tree.command(name="with-guild-inventory", description="Retire un item de l'inventaire de la guilde vers le tien")
@app_commands.describe(item_id="ID de l'item à retirer", quantite="Quantité à retirer")
async def with_guild_inventory(interaction: discord.Interaction, item_id: int, quantite: int):
    user = interaction.user
    guild_id = interaction.guild.id
    user_id = user.id

    if quantite <= 0:
        return await interaction.response.send_message("❌ La quantité doit être supérieure à 0.", ephemeral=True)

    # Vérifie la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await interaction.response.send_message("❌ Tu n'es dans aucune guilde.", ephemeral=True)

    # Vérifie l'inventaire de la guilde
    guild_item = collection36.find_one({
        "guild_id": guild_id,
        "item_id": item_id
    })

    if not guild_item or guild_item.get("quantity", 0) < quantite:
        return await interaction.response.send_message("❌ Pas assez de cet item dans l'inventaire de la guilde.", ephemeral=True)

    # Retirer les items de la guilde
    new_quantity = guild_item["quantity"] - quantite
    if new_quantity > 0:
        collection36.update_one(
            {"_id": guild_item["_id"]},
            {"$set": {"quantity": new_quantity}}
        )
    else:
        collection36.delete_one({"_id": guild_item["_id"]})

    # Ajouter les items dans l'inventaire du joueur
    insert_items = []
    for _ in range(quantite):
        insert_items.append({
            "guild_id": guild_id,
            "user_id": user_id,
            "item_id": item_id,
            "item_name": guild_item.get("item_name", "Inconnu"),
            "emoji": guild_item.get("emoji", "")
        })
    if insert_items:
        collection17.insert_many(insert_items)

    await interaction.response.send_message(
        f"📦 Tu as récupéré **{quantite}x** `{item_id}` depuis l'inventaire de la guilde.",
        ephemeral=True
    )
#----------------------------------------------- ITEMS
ITEMS = [
    {
        "id": 8,
        "emoji": "<:infini:1363615903404785734>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟙",
        "description": "L'infini protège des robs pendant 1h (utilisable 1 fois par items)",
        "price": 25000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 1h ",
        "requirements": {},
        "role_id": 1363939565336920084,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 66,
        "emoji": "<:exorciste:1363602480792994003>",
        "title": "Appel à un exorciste | 𝕊𝕆𝕀ℕ",
        "description": "Permet de retirer le nen que quelqu'un nous a posé grâce à un exorciste !",
        "price": 50000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 5,
        "tradeable": True,
        "usable": True,
        "use_effect": "Retire le rôle, faite !!heal",
        "requirements": {},
        "role_id": 1363873859912335400,
        "role_duration": 3600,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True,
        "remove_role_after_use": True
    },
    {
        "id": 88,
        "emoji": "<:infini:1363615925776941107>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟚",
        "description": "L'infini protège des robs pendant 3h (utilisable 1 fois par items)",
        "price": 50000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 3h ",
        "requirements": {},
        "role_id": 1363939567627145660,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 763,
        "emoji": "<:BomuBomunoMi:1365056026784563261>",
        "title": "Bomu Bomu no Mi",
        "description": "Permet d'exploser 10% de la banque d’un joueur ciblé chaque semaine.",
        "price": 80000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Explose 10% de la banque d’un joueur ciblé. Faite !!bombe <@user> ",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365316070172393572,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 203,
        "emoji": "<:tetsunomi:1365025648435003525>",
        "title": "Tetsu Tetsu no Mi",
        "description": "Réduit de 50% toutes les robs subies.",
        "price": 90000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Réduit de 50% toutes les robs subies.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311588139274354,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 542,
        "emoji": "<:jokijokinomi:1365019733799338064>",
        "title": "Joki Joki no Mi",
        "description": "Crée une barrière bancaire : la première attaque de la journée est entièrement annulée. Se recharge automatiquement chaque jour a 00:00. ",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Crée une barrière bancaire : la première attaque de la journée est entièrement annulée. Se recharge automatiquement chaque jour a 00:00. ",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311602290851880,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 352,
        "emoji": "<:golgolnomi:1365018965646114890>",
        "title": "Gol Gol no Mi",
        "description": "Offre un collect de 10% de sa banque chaque semaine",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Offre un collect de 10% de sa banque chaque semaine",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313257279062067,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 81,
        "emoji": "<:armure:1363599057863311412>",
        "title": "Armure du Berserker",
        "description": "Offre à son utilisateur un anti-rob de 1h... (voir description complète)",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 1h",
        "requirements": {},
        "role_id": 1363821649002238142,
        "role_duration": 3600,
        "remove_after_purchase": {
            "roles": True,
            "items": False
        }
    },
    {
        "id": 31,
        "emoji": "<:demoncontrole:1363600359611695344>",
        "title": "Contrôle de démon",
        "description": "Donne accès a tous les équipements de contrôle des démons",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a tous les équipements de contrôle des démons",
        "requirements": {},
        "role_id": 1363817629781069907,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 888,
        "emoji": "<:infini:1363615948090638490>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟛",
        "description": "L'infini protège des robs pendant 6h (utilisable 1 fois par items)",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 3h",
        "requirements": {},
        "role_id": 1363939486844850388,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 91,
        "emoji": "<:oeildemoniaque:1363947226501484746>",
        "title": "Œil démoniaque",
        "description": "Permet de voir l'avenir grâce au pouvoir de Kishirika...",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de visioner le prochain restock pendant 10 seconde",
        "requirements": {},
        "role_id": 1363949082653098094,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 553,
        "emoji": "<:haki_v1:1365669380083679252>",
        "title": "Haki de l’Armement | 𝕀𝕟𝕗𝕖𝕣𝕚𝕖𝕦𝕣",
        "description": "Offre un collect de 5,000, cooldown de 2 heures.",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Peut évoluer grâce à !!rayleigh. Vous devrez donner 100,000 à Rayleigh pour pouvoir débloquer la possibilité d'acheter le Haki de l'Armement avancé !",
        "requirements": {},
        "role_id": 1365698043684327424,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 652,
        "emoji": "<:haki_v2:1365669343685378160>",
        "title": "Haki de l’Armement | 𝔸𝕧𝕒𝕟𝕔𝕖",
        "description": "Offre un collect de 10,000, cooldown de 2 heures.",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "???",
        "requirements": {
            "roles": [1365699319163785246]
        },
        "role_id": 1365389381246124084,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 555,
        "emoji": "<:observation_v1:1365671377595535431>",
        "title": "Haki de l’Observation | 𝕀𝕟𝕗𝕖𝕣𝕚𝕖𝕦𝕣",
        "description": "Permet de connaître l'heure du prochain restock grâce à !!observation. (Cooldown : 1 semaine)",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Peut évoluer grâce à !!rayleigh. Vous devrez donner 100k à Rayleigh pour débloquer la possibilité d'acheter le Haki de l'Observation avancé !",
        "requirements": {},
        "role_id": 1365698043684327424,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 653,
        "emoji": "<:observation_v2:1365669364979728554>",
        "title": "Haki de l’Observation | 𝔸𝕧𝕒𝕟𝕔𝕖",
        "description": "Permet de connaître l'heure et le contenu du prochain restock grâce à !!Wobservation. (Cooldown : 2 semaines)",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "???",
        "requirements": {
            "roles": [1365699245377847448]
        },
        "role_id": 1365389687618928885,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 4,
        "emoji": "<:naturoermite:1363945371448905810>",
        "title": "Mode Ermite",
        "description": "Ce mode autrefois maîtrisé par Naruto lui même, il vous confère l’énergie de la nature. Grâce à cela, vous pourrez avoir plus d’ezryn !!!",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Vous donne un collect qui vous donne 5,000 <:ecoEther:1341862366249357374> toute les 2 heures",
        "requirements": {},
        "role_id": 1363948445282341135,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 7,
        "emoji": "<:licence:1363609202211422268>",
        "title": "Licence Hunter ",
        "description": "Donne accès a toutes les techniques De Hunter x Hunter, plus donne accès a un salon avec des quêtes",
        "price": 250000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne le rôle licence hunter et donne accès au nen et au quêtes destiné au hunter",
        "requirements": {},
        "role_id": 1363817603713339512,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 15,
        "emoji": "<:nen:1363607663010775300>",
        "title": "Nen | ℝ𝕆𝕃𝕃",
        "description": "Cet objet vous permet d’utiliser le Nen (attribué aléatoirement) à votre guise. Chaque technique repose sur un serment.\n— Renforcement : +renforcement donne un anti-rob de 24h (1 semaine de cooldown).\n— Émission : +emission @user maudit un joueur et lui inflige un collect de -20% (1 semaine de cooldown).\n— Manipulation : +manipulation accorde un collect de 1% toutes les 4h pendant 24h (cooldown : 1 semaine).\n— Matérialisation : +materialisation génère un objet aléatoire de la boutique (cooldown : 2 semaines).\n— Transformation : +transformation foudroie la banque d’un joueur, retirant 25% (cooldown : 2 semaines).\n— Spécialisation : donne accès à tout.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Une fois le nen utilisé celui-ci vous attribue un nen aléatoirement avec la commande !!rollnen (avec 19.9% de chance pour chaque sauf la spécialisation qui est à 0.5%)",
        "requirements": {
            "items": [7]
        },
        "role_id": 1363928528587984998,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 22,
        "emoji": "<:imperiale:1363601099990241601>",
        "title": " Arme démoniaque impériale",
        "description": "Cette objet vous permet d'utiliser le démon dans votre arme et vous permet de voler votre adversaire",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Un /roll 50 devra être fait et vous permettra de voler le pourcentage de ce roll à l’utilisateur de votre choix à condition que celui-ci soit plus riche que vous ",
        "requirements": {
            "items": [31]
        },
        "role_id": 1363817586466361514,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 45,
        "emoji": "<:hakidesrois:1363623066667843616>",
        "title": "Haki des Rois",
        "description": "Apprenez le haki des rois comme les Empereurs des mers. Faites +haki <@user> pour le paralyser ainsi il n’aura pas accès aux salons économiques",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a l'Haki des Rois",
        "requirements": {},
        "role_id": 1363817645249527879,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 28,
        "emoji": "<:rage:1363599799043227940>",
        "title": " Rage du Berserker",
        "description": "Tu perds tout contrôle. L’armure du Berserker te consume, et avec elle, ta dernière part d’humanité. Tu ne voles pas. Tu ne gagnes rien. Tu détruis, par pure haine. Ton seul objectif : voir l’ennemi ruiné.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Utilisable une seule fois avec !!berserk <@user> → roll 100, % retiré à la banque de la cible (ex : roll 67 = -67%). Nécessite l’armure du Berserker. Cooldown de 7j après achat. Objet détruit après usage.",
        "requirements": {
            "items": [81]
        },
        "role_id": 1363821333624127618,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 23,
        "emoji": "<:pokeball:1363942456676061346>",
        "title": "Pokeball",
        "description": "Cet objet vous permet de voler un objet d’une personne au hasard",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Vous donne l'accès de voler un objet au hasard de l'inventaire d'un joueur",
        "requirements": {},
        "role_id": 1363942048075481379,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 34,
        "emoji": "<:nanashimura:1363942592156405830>",
        "title": "Float",
        "description": "Vous utilisez l’un des alters provenant du One for all, et plus précisément de Nana Shimura. En l’utilisant, vous pouvez voler aussi haut que personne ne peut y accéder.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "La commande +float vous donne accès au salon (nom du salon) durant 15min mais seulement possible 1/jour.",
        "requirements": {},
        "role_id": 1363946902730575953,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 99,
        "emoji": "<:ultrainstinct:1363601650123801027>",
        "title": "Ultra Instinct ",
        "description": "Vous utilisez la forme ultime du Ultra Instinct. Vous pouvez seulement l’utiliser pendant (mettre le temps d’immunité). Lorsque vous utilisez cette forme ultime, vous anticipez toutes attaques et vous l’esquivez (donc immunisé). Malheureusement cette forme utilise énormément de votre ki, il vous faudra donc 5 jours de repos pour réutiliser cette forme",
        "price": 750000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a l'Ultra Instinct",
        "requirements": {},
        "role_id": 1363821033060307106,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 381,
        "emoji": "<:guraguranomi:1365020132048506991>",
        "title": "Gura Gura no Mi",
        "description": "Permet de créer des séismes dévastateurs à une échelle massive. Peut détruire des banques entières en faisant des secousses.",
        "price": 1000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Créer des séismes dévastateurs à une échelle massive. Détruit des banques entières en faisant des secousses.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313248269828116,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 666,
        "emoji": "<:MarshallDTeach:1365695681028821093>",
        "title": "Marshall D. Teach",
        "description": "Permet de posséder 2 Fruits du Démon a la fois.",
        "price": 1000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de posséder 2 Fruits du Démon a la fois.",
        "requirements": {},
        "role_id": 1365310665417556011,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 911,
        "emoji": "<:hiehienomi:1365020469547503698>",
        "title": "Hie Hie no Mi",
        "description": "Permet de geler le temps et les actions économiques des autres joueurs, le joueur ciblé n'a plus accès à l'économie",
        "price": 1800000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de geler le temps et les actions économiques des autres joueurs, le joueur ciblé n'a plus accès à l'économie.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311608259346462,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 797,
        "emoji": "<:yamiyaminomi:1365020675450081280>",
        "title": "Yami Yami no Mi",
        "description": "Absorbe tous les vols subis et les renvoie avec une puissance doublée (200%).\n-Bénéficie de 6 heures de protection. Rétablissement en 24h.",
        "price": 2500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Absorbe les vols et les renvoie avec 200% de puissance. 6h de protection, 24h de cooldown.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313251201519697,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 229,
        "emoji": "<:gomugomunomi:1365020813543215137>",
        "title": "Gomu Gomu no Mi",
        "description": "Permet de rendre ta banque extensible et malléable, quasiment indestructible. Tu peux l’étirer à volonté pour éviter toute perte.",
        "price": 3000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Renvoie 150% des attaques bancaires, booste tes revenus de 5% (1 semaine) et bloque/renvoie 300% des attaques tout en doublant les revenus (24h).",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311611019202744,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 469,
        "emoji": "<:nikanikanomi:1365021787015876760>",
        "title": "Nika Nika no Mi",
        "description": "Le Fruit de Nika te confère des pouvoirs légendaires, au-delà de tout ce qui est imaginable, te permettant de réécrire les règles économiques et manipuler la réalité des finances à ta guise.",
        "price": 7000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Le Nika Nika no Mi permet de créer des ressources, effacer dettes, et avec Gear Fifth, booste tes fonds de 500% et influe sur l'économie des autres.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311614332571739, 1365313292477927464],
        "requirements": {
            "roles": [1365311611019202744]
        },
        "role_id": 1365313292477927464,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 672,
        "emoji": "<:uouonomi:1365021938849677403>",
        "title": "Uo Uo no Mi, Modèle : Seiryu",
        "description": "Un fruit mythique qui permet à son utilisateur de se transformer en un dragon céleste, une créature d’une force inégalée, capable de manipuler les éléments et la destruction à une échelle dévastatrice. Ce fruit confère à son possesseur un pouvoir colossal, comparable à un typhon divin.",
        "price": 10000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Le **Uo Uo no Mi, Seiryu** transforme en dragon céleste, protège la banque (30% vol max) pendant 1 semaine, lance des flammes dévastatrices (vol de 75%) et invoque un orage réduisant les gains de 70% et renvoyant les attaques contre toi. *Colère Draconique* détruit l'économie d'un joueur une fois par mois.",
        "requirements": {},
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "role_id": 1365311614332571739,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 202,
        "emoji": "<:bc1s1:1364217784439144488>",
        "title": "Boule de Cristal n°1",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 197,
        "emoji": "<:bc2s1:1364224502996930642>",
        "title": "Boule de Cristal n°2",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 425,
        "emoji": "<:bc3s1:1364224526476640306>",
        "title": "Boule de Cristal n°3",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 736,
        "emoji": "<:bc4s1:1364224543937396746>",
        "title": "Boule de Cristal n°4",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 872,
        "emoji": "<:bc5s1:1364224573306048522>",
        "title": "Boule de Cristal n°5",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 964,
        "emoji": "<:bc6s1:1364224591488221276>",
        "title": "Boule de Cristal n°6",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 987,
        "emoji": "<:bc7s1:1364224611536994315>",
        "title": "Boule de Cristal n°7",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 993,
        "emoji": "<:luffy:1367570815188729877>",
        "title": "Pièce Luffy",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 221,
        "emoji": "<:zoro:1367570671244279912>",
        "title": "Pièce Zoro",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 621,
        "emoji": "<:sanji:1367570434752778270>",
        "title": "Pièce Sanji",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 413,
        "emoji": "<:nami:1367570885661429790>",
        "title": "Pièce Nami",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 280,
        "emoji": "<:usopp:1367570730392223804>",
        "title": "Pièce Usopp",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 682,
        "emoji": "<:chopper:1367570848549965935>",
        "title": "Pièce Chopper",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 573,
        "emoji": "<:robin:1367570558581084231>",
        "title": "Pièce Robin",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 132,
        "emoji": "<:franky:1367570517674033183>",
        "title": "Pièce Franky",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 856,
        "emoji": "<:jinbe:1367570481720332448>",
        "title": "Pièce Jinbe",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 869,
        "emoji": "<:brook:1367570627157954660>",
        "title": "Pièce Brook",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
]

# Fonction pour insérer les items dans MongoDB
def insert_items_into_db():
    for item in ITEMS:
        if not collection16.find_one({"id": item["id"]}):
            collection16.insert_one(item)

def get_page_embed(page: int, items_per_page=10):
    start = page * items_per_page
    end = start + items_per_page
    items = ITEMS[start:end]

    embed = discord.Embed(title="🛒 Boutique", color=discord.Color.blue())

    for item in items:
        formatted_price = f"{item['price']:,}".replace(",", " ")
        name_line = f"ID: {item['id']} | {formatted_price} {item['emoji_price']} - {item['title']} {item['emoji']}"

        # Seulement la description, sans les "requirements" et "bonus"
        value = item["description"]

        embed.add_field(name=name_line, value=value, inline=False)

    total_pages = (len(ITEMS) - 1) // items_per_page + 1
    embed.set_footer(text=f"Page {page + 1}/{total_pages}")
    return embed

# Vue pour les boutons de navigation
class Paginator(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.page = 0
        self.user = user

    async def update(self, interaction: discord.Interaction):
        embed = get_page_embed(self.page)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Tu n'as pas la permission de naviguer dans ce menu.",
                color=discord.Color.red()
            )
            return await interaction.response.edit_message(embed=embed, view=self)
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Tu n'as pas la permission de naviguer dans ce menu.",
                color=discord.Color.red()
            )
            return await interaction.response.edit_message(embed=embed, view=self)
        if (self.page + 1) * 10 < len(ITEMS):
            self.page += 1
            await self.update(interaction)

# Fonction de vérification des requirements (rôles et items)
async def check_requirements(user: discord.Member, requirements: dict):
    # Vérifier les rôles requis
    if "roles" in requirements:
        user_roles = [role.id for role in user.roles]
        for role_id in requirements["roles"]:
            if role_id not in user_roles:
                return False, f"Tu n'as pas le rôle requis <@&{role_id}>."

    # Vérifier les items requis (dans un système de base de données par exemple)
    if "items" in requirements:
        for item_id in requirements["items"]:
            item_in_inventory = await check_user_has_item(user, item_id)  # Fonction fictive à implémenter
            if not item_in_inventory:
                return False, f"Tu n'as pas l'item requis ID:{item_id}."

    return True, "Requirements vérifiés avec succès."

# Fonction d'achat d'un item
async def buy_item(user: discord.Member, item_id: int):
    # Chercher l'item dans la boutique
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        return f"L'item avec l'ID {item_id} n'existe pas."

    # Vérifier les requirements
    success, message = await check_requirements(user, item["requirements"])
    if not success:
        return message

    # Vérifier si le rôle doit être ajouté ou supprimé après l'achat
    if item["remove_after_purchase"]["roles"]:
        role = discord.utils.get(user.guild.roles, id=item["role_id"])
        if role:
            await user.remove_roles(role)
            return f"Le rôle {role.name} a été supprimé après l'achat de {item['title']}."

    if item["remove_after_purchase"]["items"]:
        # Logique pour supprimer l'item (par exemple, de l'inventaire du joueur)
        pass

    return f"L'achat de {item['title']} a été effectué avec succès."

# Slash command /item-store
@bot.tree.command(name="item-store", description="Affiche la boutique d'items")
async def item_store(interaction: discord.Interaction):
    embed = get_page_embed(0)
    view = Paginator(user=interaction.user)
    await interaction.response.send_message(embed=embed, view=view)

# Appel de la fonction pour insérer les items dans la base de données lors du démarrage du bot
insert_items_into_db()

from discord import app_commands
from discord.ext import commands
import discord

async def item_autocomplete(interaction: discord.Interaction, current: str):
    # On filtre les items qui contiennent ce que l'utilisateur est en train d'écrire
    results = []
    for item in ITEMS:
        if current.lower() in item["title"].lower():
            results.append(app_commands.Choice(name=item["title"], value=item["title"]))

    # On limite à 25 résultats max (Discord ne permet pas plus)
    return results[:25]

# Commande d'achat avec recherche par nom d'item
@bot.tree.command(name="item-buy", description="Achète un item de la boutique via son nom.")
@app_commands.describe(item_name="Nom de l'item à acheter", quantity="Quantité à acheter (défaut: 1)")
@app_commands.autocomplete(item_name=item_autocomplete)  # Lier l'autocomplétion à l'argument item_name
async def item_buy(interaction: discord.Interaction, item_name: str, quantity: int = 1):
    user_id = interaction.user.id
    guild_id = interaction.guild.id

    # Chercher l'item en utilisant le nom récupéré via l'autocomplétion
    item = collection16.find_one({"title": item_name})
    if not item:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Aucun item avec ce nom n'a été trouvé dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if quantity <= 0:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité invalide",
            description="La quantité doit être supérieure à zéro.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if item.get("quantity", 0) < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Stock insuffisant",
            description=f"Il ne reste que **{item.get('quantity', 0)}x** de cet item en stock.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Vérifier les requirements avant de permettre l'achat
    valid, message = await check_requirements(interaction.user, item.get("requirements", {}))
    if not valid:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Prérequis non remplis",
            description=message,
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    user_data = collection.find_one({"user_id": user_id, "guild_id": guild_id}) or {"cash": 0}
    total_price = int(item["price"]) * quantity

    if user_data.get("cash", 0) < total_price:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Fonds insuffisants",
            description=f"Tu n'as pas assez de <:ecoEther:1341862366249357374> pour cet achat.\nPrix total : **{total_price:,}**",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Retirer l'argent du joueur
    collection.update_one(
        {"user_id": user_id, "guild_id": guild_id},
        {"$inc": {"cash": -total_price}},
        upsert=True
    )

    # Mise à jour de l'inventaire simple (collection7)
    inventory_data = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
    if inventory_data:
        inventory = inventory_data.get("items", {})
        inventory[str(item["id"])] = inventory.get(str(item["id"]), 0) + quantity
        collection7.update_one(
            {"user_id": user_id, "guild_id": guild_id},
            {"$set": {"items": inventory}}
        )
    else:
        collection7.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "items": {str(item["id"]): quantity}
        })

    # Mise à jour de l'inventaire structuré (collection17)
    documents = [{
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": item["id"],
        "item_name": item["title"],
        "emoji": item.get("emoji"),
        "price": item["price"],
        "acquired_at": datetime.utcnow()
    } for _ in range(quantity)]
    if documents:
        collection17.insert_many(documents)

    # Mise à jour du stock boutique
    collection16.update_one(
        {"id": item["id"]},
        {"$inc": {"quantity": -quantity}}
    )

    # Gestion de la suppression des rôles et items après achat
    if item.get("remove_after_purchase"):
        remove_config = item["remove_after_purchase"]

        if remove_config.get("roles", False) and item.get("role_id"):
            role = discord.utils.get(interaction.guild.roles, id=item["role_id"])
            if role:
                await interaction.user.remove_roles(role)
                print(f"Rôle {role.name} supprimé pour {interaction.user.name} après l'achat.")

        if remove_config.get("items", False):
            inventory_data = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
            if inventory_data:
                inventory = inventory_data.get("items", {})
                if str(item["id"]) in inventory:
                    inventory[str(item["id"])] -= quantity
                    if inventory[str(item["id"])] <= 0:
                        del inventory[str(item["id"])]
                    collection7.update_one(
                        {"user_id": user_id, "guild_id": guild_id},
                        {"$set": {"items": inventory}}
                    )
                    print(f"{quantity} de l'item {item['title']} supprimé de l'inventaire de {interaction.user.name}.")

    # Envoi du message de succès
    embed = discord.Embed(
        title="<:Check:1362710665663615147> Achat effectué",
        description=(
            f"Tu as acheté **{quantity}x {item['title']}** {item.get('emoji', '')} "
            f"pour **{total_price:,}** {item.get('emoji_price', '')} !"
        ),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="item-inventory", description="Affiche l'inventaire d'un utilisateur")
async def item_inventory(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    guild_id = interaction.guild.id

    # Curseur synchrone avec pymongo
    items_cursor = collection17.find({"guild_id": guild_id, "user_id": user.id})

    item_counts = {}
    item_details = {}

    for item in items_cursor:
        item_id = item["item_id"]
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
        if item_id not in item_details:
            item_details[item_id] = {
                "title": item.get("item_name", "Nom inconnu"),
                "emoji": item.get("emoji", ""),
            }

    # Bleu doux (ex : #89CFF0)
    soft_blue = discord.Color.from_rgb(137, 207, 240)

    embed = discord.Embed(
        title="Use an item with the /item-use command.",
        color=soft_blue
    )

    embed.set_author(name=user.name, icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

    if not item_counts:
        embed.title = "<:classic_x_mark:1362711858829725729> Inventaire vide"
        embed.description = "Use an item with the `/item-use` command."
        embed.color = discord.Color.red()
    else:
        lines = []
        for item_id, quantity in item_counts.items():
            details = item_details[item_id]
            lines.append(f"**{quantity}x** {details['title']} {details['emoji']} (ID: `{item_id}`)")
        embed.description = "\n".join(lines)

    await interaction.response.send_message(embed=embed)

from typing import List

async def item_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    results = []
    items = list(collection16.find().limit(100))  # Charger les 100 premiers items de la collection

    for item in items:
        title = item.get("title", "Sans nom")
        
        # On vérifie si l'input actuel de l'utilisateur est dans le nom de l'item
        if current.lower() in title.lower():
            results.append(app_commands.Choice(name=title, value=title))

    return results[:25]  # On limite à 25 résultats

@bot.tree.command(name="item-info", description="Affiche toutes les informations d'un item de la boutique")
@app_commands.describe(id="Nom de l'item à consulter")
@app_commands.autocomplete(id=item_autocomplete)  # <-- On associe l'autocomplétion ici
async def item_info(interaction: discord.Interaction, id: str):
    # On cherche l'item par le nom
    item = collection16.find_one({"title": id})

    if not item:
        embed = discord.Embed(
            title="❌ Item introuvable",
            description="Aucun item trouvé avec ce nom.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    formatted_price = f"{item['price']:,}".replace(",", " ")

    embed = discord.Embed(
        title=f"📦 Détails de l'item : {item['title']}",
        color=discord.Color.blue()
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

    embed.add_field(name="**Nom de l'item**", value=item['title'], inline=False)
    embed.add_field(name="**Description**", value=item['description'], inline=False)
    embed.add_field(name="ID", value=str(item['id']), inline=True)
    embed.add_field(name="Prix", value=f"{formatted_price} {item['emoji_price']}", inline=True)
    embed.add_field(name="Quantité", value=str(item.get('quantity', 'Indisponible')), inline=True)

    tradeable = "✅ Oui" if item.get("tradeable", False) else "❌ Non"
    usable = "✅ Oui" if item.get("usable", False) else "❌ Non"
    embed.add_field(name="Échangeable", value=tradeable, inline=True)
    embed.add_field(name="Utilisable", value=usable, inline=True)

    if item.get("use_effect"):
        embed.add_field(name="Effet à l'utilisation", value=item["use_effect"], inline=False)

    if item.get("requirements"):
        requirements = item["requirements"]
        req_message = []

        if "roles" in requirements:
            for role_id in requirements["roles"]:
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                if role:
                    req_message.append(f"• Rôle requis : <@&{role_id}> ({role.name})")
                else:
                    req_message.append(f"• Rôle requis : <@&{role_id}> (Introuvable)")

        if "items" in requirements:
            for required_item_id in requirements["items"]:
                item_in_inventory = await check_user_has_item(interaction.user, required_item_id)
                if item_in_inventory:
                    req_message.append(f"• Item requis : ID {required_item_id} (Possédé)")
                else:
                    req_message.append(f"• Item requis : ID {required_item_id} (Non possédé)")

        embed.add_field(
            name="Prérequis",
            value="\n".join(req_message) if req_message else "Aucun prérequis",
            inline=False
        )
    else:
        embed.add_field(name="Prérequis", value="Aucun prérequis", inline=False)

    emoji = item.get("emoji")
    if emoji:
        try:
            emoji_id = emoji.split(":")[2].split(">")[0]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji_id}.png")
        except Exception as e:
            print(f"Erreur lors de l'extraction de l'emoji : {e}")

    embed.set_footer(text="🛒 Etherya • Détails de l'item")

    await interaction.response.send_message(embed=embed)

from typing import List

async def item_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    user = interaction.user
    user_id = user.id
    guild_id = interaction.guild.id

    # Chercher les items dans l'inventaire de l'utilisateur
    owned_items = collection17.find({"user_id": user_id, "guild_id": guild_id})
    
    results = []
    
    for owned_item in owned_items:
        item_id = owned_item["item_id"]
        item_data = collection16.find_one({"id": item_id})
        
        if item_data and current.lower() in item_data["title"].lower():
            results.append(app_commands.Choice(name=item_data["title"], value=str(item_id)))
    
    return results[:25]  # Limiter à 25 résultats

@bot.tree.command(name="item-use", description="Utilise un item de ton inventaire.")
@app_commands.describe(item_id="Nom de l'item à utiliser")
@app_commands.autocomplete(item_id=item_autocomplete)  # <-- On ajoute l'autocomplétion ici
async def item_use(interaction: discord.Interaction, item_id: int):
    user = interaction.user
    user_id = user.id
    guild = interaction.guild
    guild_id = guild.id

    # Vérifie si l'item est dans l'inventaire
    owned_item = collection17.find_one({"user_id": user_id, "guild_id": guild_id, "item_id": item_id})
    if not owned_item:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item non possédé",
            description="Tu ne possèdes pas cet item dans ton inventaire.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Récupère les infos de l'item
    item_data = collection16.find_one({"id": item_id})
    if not item_data or not item_data.get("usable", False):
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Utilisation impossible",
            description="Cet item n'existe pas ou ne peut pas être utilisé.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Vérifier si l'utilisateur a le rôle spécifique qui permet d'utiliser des items malgré les rôles bloquants
    special_role_id = 1365310665417556011
    if special_role_id in [role.id for role in user.roles]:
        embed = discord.Embed(
            title=f"<:Check:1362710665663615147> Utilisation de l'item",
            description=f"Tu as utilisé **{item_data['title']}** {item_data.get('emoji', '')}, malgré les restrictions de rôle.",
            color=discord.Color.green()
        )
        return await interaction.response.send_message(embed=embed)

    # Vérification des rôles bloquants
    if item_data.get("blocked_roles"):
        blocked_roles = item_data["blocked_roles"]
        
        # Compter combien de rôles bloquants l'utilisateur possède
        user_blocked_roles = [role for role in user.roles if role.id in blocked_roles]
        
        # Vérification si l'utilisateur a le rôle spécial qui permet de dépasser la limite
        special_role_id = 1365310665417556011
        limit = 1  # Limite par défaut si l'utilisateur n'a pas le rôle spécial
        
        if special_role_id in [role.id for role in user.roles]:
            limit = 2  # Si l'utilisateur a le rôle spécial, on augmente la limite à 2

        # Si l'utilisateur a trop de rôles bloquants (>= limite), on bloque l'utilisation
        if len(user_blocked_roles) >= limit:
            embed = discord.Embed(
                title="<:classic_x_mark:1362711858829725729> Utilisation bloquée",
                description="Tu ne peux pas utiliser cet item en raison de tes rôles bloquants.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed)

    # Si aucun rôle ne bloque, continuer normalement (comme dans ton code actuel)
    # Supprime un exemplaire dans l'inventaire
    collection17.delete_one({
        "user_id": user_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    embed = discord.Embed(
        title=f"<:Check:1362710665663615147> Utilisation de l'item",
        description=f"Tu as utilisé **{item_data['title']}** {item_data.get('emoji', '')}.",
        color=discord.Color.green()
    )

    # Ajout du rôle si défini
    role_id = item_data.get("role_id")
    if role_id:
        role = guild.get_role(int(role_id))
        if role:
            # Vérification de la hiérarchie des rôles
            if interaction.guild.me.top_role.position > role.position:
                try:
                    await user.add_roles(role)
                    embed.add_field(name="🎭 Rôle attribué", value=f"Tu as reçu le rôle **{role.name}**.", inline=False)
                except discord.Forbidden:
                    embed.add_field(
                        name="⚠️ Rôle non attribué",
                        value="Je n’ai pas la permission d’attribuer ce rôle. Vérifie mes permissions ou la hiérarchie des rôles.",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="⚠️ Rôle non attribué",
                    value="Le rôle est trop élevé dans la hiérarchie pour que je puisse l’attribuer.",
                    inline=False
                )

    # Ajout d'un item bonus s'il y en a
    reward_item_id = item_data.get("gives_item_id")
    if reward_item_id:
        collection17.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": reward_item_id
        })
        reward_data = collection16.find_one({"id": reward_item_id})
        if reward_data:
            reward_title = reward_data["title"]
            reward_emoji = reward_data.get("emoji", "")
            embed.add_field(name="🎁 Récompense reçue", value=f"Tu as reçu **{reward_title}** {reward_emoji}.", inline=False)

    # Gestion de la suppression après utilisation
    if item_data.get("remove_after_use"):
        if item_data["remove_after_use"].get("roles", False):
            role = discord.utils.get(interaction.guild.roles, id=item_data["role_id"])
            if role and role in user.roles:
                await user.remove_roles(role)
                embed.add_field(name="⚠️ Rôle supprimé", value=f"Le rôle **{role.name}** a été supprimé après l'utilisation de l'item.", inline=False)
                print(f"Rôle {role.name} supprimé pour {interaction.user.name} après l'utilisation de l'item.")
        
        if item_data["remove_after_use"].get("items", False):
            collection17.delete_one({
                "user_id": user_id,
                "guild_id": guild_id,
                "item_id": item_id
            })
            print(f"Item ID {item_id} supprimé de l'inventaire de {interaction.user.name}.")

    await interaction.response.send_message(embed=embed)


from discord.app_commands import Choice, autocomplete

# Fonction d'autocomplétion pour l'ID des items
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Recherche parmi les items dans la collection
    items = collection16.find()
    
    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in items:
        if current.lower() in item["title"].lower():
            results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-give", description="(Admin) Donne un item à un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui donner l'item",
    item_id="ID de l'item à donner",
    quantity="Quantité d'items à donner"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_give(interaction: discord.Interaction, member: discord.Member, item_id: int, quantity: int = 1):
    guild_id = interaction.guild.id
    user_id = member.id

    # Vérifie si l'item existe dans la boutique
    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    if quantity < 1:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité invalide",
            description="La quantité doit être d'au moins **1**.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Ajoute l'item dans la collection17 (inventaire structuré)
    for _ in range(quantity):
        collection17.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": item_id,
            "item_name": item_data["title"],
            "emoji": item_data.get("emoji", ""),
            "price": item_data.get("price"),
            "acquired_at": datetime.utcnow()
        })

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    embed = discord.Embed(
        title=f"<:Check:1362710665663615147> Item donné",
        description=f"**{quantity}x {item_name}** {emoji} ont été donnés à {member.mention}.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour l'ID des items
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Recherche parmi les items dans la collection
    items = collection16.find()
    
    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in items:
        if current.lower() in item["title"].lower():
            results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-take", description="(Admin) Retire un item d'un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui retirer l'item",
    item_id="ID de l'item à retirer",
    quantity="Quantité d'items à retirer"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_take(interaction: discord.Interaction, member: discord.Member, item_id: int, quantity: int = 1):
    guild_id = interaction.guild.id
    user_id = member.id

    # Vérifie si l'item existe
    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    # Vérifie combien l'utilisateur en possède
    owned_count = collection17.count_documents({
        "user_id": user_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    if owned_count < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité insuffisante",
            description=f"{member.mention} ne possède que **{owned_count}x {item_name}** {emoji}. Impossible de retirer {quantity}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Supprime les exemplaires un par un
    for _ in range(quantity):
        collection17.delete_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": item_id
        })

    embed = discord.Embed(
        title="<:Check:1362710665663615147> Item retiré",
        description=f"**{quantity}x {item_name}** {emoji} ont été retirés de l'inventaire de {member.mention}.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour l'ID des items, filtrée par l'inventaire de l'utilisateur
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    # Recherche des items que le joueur possède dans son inventaire
    owned_items = collection17.find({"user_id": user_id, "guild_id": guild_id})

    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in owned_items:
        item_data = collection16.find_one({"id": item["item_id"]})
        if item_data and current.lower() in item_data["title"].lower():
            results.append(Choice(name=f"{item_data['title']} (ID: {item_data['id']})", value=item_data['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-sell", description="Vends un item à un autre utilisateur pour un prix donné.")
@app_commands.describe(
    member="L'utilisateur à qui vendre l'item",
    item_id="ID de l'item à vendre",
    price="Prix de vente de l'item",
    quantity="Quantité d'items à vendre (par défaut 1)"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_sell(interaction: discord.Interaction, member: discord.User, item_id: int, price: int, quantity: int = 1):
    guild_id = interaction.guild.id
    seller_id = interaction.user.id
    buyer_id = member.id

    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    owned_count = collection17.count_documents({
        "user_id": seller_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    if owned_count < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Vente impossible",
            description=f"Tu ne possèdes que **{owned_count}x {item_name}** {emoji}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    buyer_data = collection.find_one({"guild_id": guild_id, "user_id": buyer_id}) or {"cash": 1500}
    total_price = price * quantity

    # Vérification du cash uniquement
    if buyer_data.get("cash", 0) < total_price:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Fonds insuffisants",
            description=f"{member.mention} n'a pas assez d'argent en **cash** pour acheter **{quantity}x {item_name}** {emoji}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Boutons
    class SellView(View):
        def __init__(self):
            super().__init__(timeout=60)

        @discord.ui.button(label="✅ Accepter", style=discord.ButtonStyle.green)
        async def accept_sell(self, interaction_btn: discord.Interaction, button: Button):
            if interaction_btn.user.id != buyer_id:
                return await interaction_btn.response.send_message("❌ Ce n'est pas ton offre.", ephemeral=True)

            # Transfert de l'item
            for _ in range(quantity):
                collection17.insert_one({
                    "user_id": buyer_id,
                    "guild_id": guild_id,
                    "item_id": item_id,
                    "item_name": item_name,
                    "emoji": emoji,
                    "price": price,
                    "acquired_at": datetime.utcnow()
                })
                collection17.delete_one({
                    "user_id": seller_id,
                    "guild_id": guild_id,
                    "item_id": item_id
                })

            # Paiement
            collection.update_one(
                {"guild_id": guild_id, "user_id": buyer_id},
                {"$inc": {"cash": -total_price}},  # Décrémentation du cash de l'acheteur
                upsert=True
            )
            collection.update_one(
                {"guild_id": guild_id, "user_id": seller_id},
                {"$inc": {"cash": total_price}},  # Ajout du cash au vendeur
                upsert=True
            )

            confirm_embed = discord.Embed(
                title="<:Check:1362710665663615147> Vente conclue",
                description=f"{member.mention} a acheté **{quantity}x {item_name}** {emoji} pour **{total_price:,}** <:ecoEther:1341862366249357374>.",
                color=discord.Color.green()
            )
            await interaction_btn.response.edit_message(embed=confirm_embed, view=None)

        @discord.ui.button(label="❌ Refuser", style=discord.ButtonStyle.red)
        async def decline_sell(self, interaction_btn: discord.Interaction, button: Button):
            if interaction_btn.user.id != buyer_id:
                return await interaction_btn.response.send_message("❌ Ce n'est pas ton offre.", ephemeral=True)

            cancel_embed = discord.Embed(
                title="<:classic_x_mark:1362711858829725729> Offre refusée",
                description=f"{member.mention} a refusé l'offre.",
                color=discord.Color.red()
            )
            await interaction_btn.response.edit_message(embed=cancel_embed, view=None)

    view = SellView()

    offer_embed = discord.Embed(
        title=f"💸 Offre de {interaction.user.display_name}",
        description=f"{interaction.user.mention} te propose **{quantity}x {item_name}** {emoji} pour **{total_price:,}** <:ecoEther:1341862366249357374>.",
        color=discord.Color.gold()
    )
    offer_embed.set_footer(text="Tu as 60 secondes pour accepter ou refuser.")

    await interaction.response.send_message(embed=offer_embed, content=member.mention, view=view)

# Fonction d'autocomplétion pour les items disponibles en boutique
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Cherche tous les items de la boutique qui correspondent à ce que tape l'utilisateur
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="item-leaderboard", description="Affiche le leaderboard des utilisateurs possédant un item spécifique.")
@app_commands.describe(
    item_id="ID de l'item dont vous voulez voir le leaderboard"
)
@app_commands.autocomplete(item_id=item_shop_autocomplete)  # <<<<<< ajoute ici l'autocomplete
async def item_leaderboard(interaction: discord.Interaction, item_id: int):
    guild = interaction.guild
    guild_id = guild.id

    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Aucun item n'existe avec cet ID.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    item_emoji = item_data.get("emoji", "")

    # Agrégation des quantités par utilisateur
    pipeline = [
        {"$match": {"guild_id": guild_id, "item_id": item_id}},
        {"$group": {"_id": "$user_id", "quantity": {"$sum": 1}}},
        {"$sort": {"quantity": -1}},
        {"$limit": 10}
    ]
    leaderboard = list(collection17.aggregate(pipeline))

    if not leaderboard:
        embed = discord.Embed(
            title="📉 Aucun résultat",
            description=f"Aucun utilisateur ne possède **{item_name}** {item_emoji} dans ce serveur.",
            color=discord.Color.dark_grey()
        )
        return await interaction.response.send_message(embed=embed)

    embed = discord.Embed(
        title=f"🏆 Leaderboard : {item_name} {item_emoji}",
        description="Classement des membres qui possèdent le plus cet item :",
        color=discord.Color.blurple()
    )

    for i, entry in enumerate(leaderboard, start=1):
        user = guild.get_member(entry["_id"])
        name = user.display_name if user else f"<Utilisateur inconnu `{entry['_id']}`>"
        embed.add_field(
            name=f"{i}. {name}",
            value=f"{entry['quantity']}x {item_name} {item_emoji}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour les items de la boutique (déjà faite, donc on réutilise !)
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="restock", description="Restock un item dans la boutique")
@app_commands.describe(
    item_id="ID de l'item à restock",
    quantity="Nouvelle quantité à définir"
)
@app_commands.autocomplete(item_id=item_shop_autocomplete)  # <<<< ajoute ici l'autocomplete
async def restock(interaction: discord.Interaction, item_id: int, quantity: int):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    item = collection16.find_one({"id": item_id})
    if not item:
        return await interaction.response.send_message(f"❌ Aucun item trouvé avec l'ID {item_id}.", ephemeral=True)

    collection16.update_one({"id": item_id}, {"$set": {"quantity": quantity}})
    return await interaction.response.send_message(
        f"✅ L'item **{item['title']}** a bien été restocké à **{quantity}** unités.", ephemeral=True
    )

# Même autocomplétion que pour /restock (items de la boutique)
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(app_commands.Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="reset-item", description="Supprime tous les items de la boutique")
async def reset_item(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    deleted = collection16.delete_many({})  # Supprime tous les documents de la collection

    return await interaction.response.send_message(
        f"🗑️ {deleted.deleted_count} item(s) ont été supprimés de la boutique.", ephemeral=True
    )

@bot.tree.command(name="delete-item", description="Supprime un item spécifique de la boutique")
@app_commands.describe(item_id="L'identifiant de l'item à supprimer")
async def delete_item(interaction: discord.Interaction, item_id: str):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    result = collection16.delete_one({"id": item_id})

    if result.deleted_count == 0:
        return await interaction.response.send_message("❌ Aucun item trouvé avec cet ID.", ephemeral=True)

    return await interaction.response.send_message(f"🗑️ L'item avec l'ID `{item_id}` a été supprimé de la boutique.", ephemeral=True)

#-------------------------------------------------------- Badges

BADGES = [
    {
        "id": 1,
        "emoji": "<:hxh:1363923320256463088>",
        "title": "Badge Hunter X Hunter",
        "description": "Badge Collector.",
        "price": 100,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 10,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 2,
        "emoji": "<:gon:1363923253134889082>",
        "title": "Badge Gon",
        "description": "Badge Collector",
        "price": 150,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 5,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 3,
        "emoji": "<:onepiece:1364713455981957260>",
        "title": "Badge One Piece",
        "description": "Badge Collector.",
        "price": 200,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 4,
        "emoji": "<:luffy:1364713438768533585>",
        "title": "Badge Luffy",
        "description": "Badge Collector.",
        "price": 250,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
]

# Fonction pour obtenir les badges dans un format de page avec pagination
def get_badge_embed(page: int = 0, items_per_page=10):
    start = page * items_per_page
    end = start + items_per_page
    badges_page = BADGES[start:end]

    embed = discord.Embed(title="🛒 Boutique de Badges", color=discord.Color.purple())

    for badge in badges_page:
        formatted_price = f"{badge['price']:,}".replace(",", " ")
        name_line = f"ID: {badge['id']} | {formatted_price} {badge['emoji_price']} - {badge['title']} {badge['emoji']}"

        # Seulement la description, sans les "requirements" et "bonus"
        value = badge["description"]

        embed.add_field(name=name_line, value=value, inline=False)

    total_pages = (len(BADGES) - 1) // items_per_page + 1
    embed.set_footer(text=f"Page {page + 1}/{total_pages}")
    return embed

# Vue pour les boutons de navigation
class BadgePaginator(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.page = 0
        self.user = user

    async def update(self, interaction):
        embed = get_badge_embed(self.page)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction, button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Tu ne peux pas utiliser ces boutons.", ephemeral=True)
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction, button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Tu ne peux pas utiliser ces boutons.", ephemeral=True)
        if (self.page + 1) * 10 < len(BADGES):
            self.page += 1
            await self.update(interaction)

# Commande pour afficher la boutique de badges
@bot.tree.command(name="badge-store", description="Affiche la boutique de badges")
async def badge_store(interaction: discord.Interaction):
    view = BadgePaginator(interaction.user)
    embed = get_badge_embed(0)  # Initial page (0)
    await interaction.channel.send(embed=embed, view=view)  # Envoi à tout le monde dans le canal

# Fonction pour insérer les badges dans la base de données lors du démarrage du bot
def insert_badge_into_db():
    for badge in BADGES:
        if not collection19.find_one({"id": badge["id"]}):
            collection19.insert_one(badge)

# Appel de la fonction pour insérer les badges dans la base de données lors du démarrage du bot
insert_badge_into_db()

from discord import app_commands

@app_commands.autocomplete(badge_id=True)
async def badge_autocomplete_by_name(interaction: discord.Interaction, current: str):
    results = collection19.find(
        {"title": {"$regex": f"^{current}", "$options": "i"}}
    ).limit(20)

    choices = []
    for badge in results:
        title = badge.get("title", "Sans titre")
        emoji = badge.get("emoji", "")
        badge_id = badge["id"]
        # Le name est affiché, le value est ce qui sera envoyé à la commande
        choices.append(app_commands.Choice(name=f"{title} {emoji} (ID: {badge_id})", value=badge_id))

    return choices

@bot.tree.command(name="badge-give", description="(Admin) Donne un badge à un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui donner le badge",
    badge_id="Badge à donner (autocomplete par nom)"
)
@app_commands.autocomplete(badge_id=badge_autocomplete_by_name)
async def badge_give(interaction: discord.Interaction, member: discord.Member, badge_id: int):
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    user_data = collection20.find_one({"user_id": member.id})
    if user_data and badge_id in user_data.get("badges", []):
        embed = discord.Embed(
            title="❌ Badge déjà possédé",
            description=f"{member.mention} possède déjà ce badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    collection20.update_one(
        {"user_id": member.id},
        {"$addToSet": {"badges": badge_id}},
        upsert=True
    )

    embed = discord.Embed(
        title="🎖️ Badge donné",
        description=f"Le badge **{badge['title']}** {badge['emoji']} a été donné à {member.mention}.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="badge-inventory", description="Affiche les badges de l'inventaire d'un utilisateur.")
async def badge_inventory(interaction: discord.Interaction):
    # Récupérer les données de l'utilisateur
    user_data = collection20.find_one({"user_id": interaction.user.id})
    
    if not user_data or not user_data.get("badges"):
        embed = discord.Embed(
            title="❌ Aucun badge trouvé",
            description="Tu ne possèdes aucun badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Récupérer les badges de l'utilisateur
    badge_ids = user_data["badges"]
    badges = collection19.find({"id": {"$in": badge_ids}})

    embed = discord.Embed(title=f"Inventaire de Badges de {interaction.user.display_name}", color=discord.Color.blue())

    if badges:
        for badge in badges:
            embed.add_field(
                name=f"{badge['emoji']} {badge['title']}",
                value=f"{badge['description']}\nPrix: {badge['price']} {badge['emoji_price']}",
                inline=False
            )
    else:
        embed.add_field(
            name="Aucun badge trouvé",
            value="Tu ne possèdes aucun badge.",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# Fonction pour récupérer le leaderboard des utilisateurs ayant un badge spécifique
@bot.tree.command(name="badge-leaderboard", description="Affiche le classement des utilisateurs ayant un badge spécifique.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(badge_id="Badge à filtrer")
@app_commands.autocomplete(badge_id=badge_autocomplete_by_name)  # Utilisation de l'autocomplétion pour le badge
async def badge_leaderboard(interaction: discord.Interaction, badge_id: int):
    # Récupérer les utilisateurs qui ont ce badge spécifique
    leaderboard = collection20.find({"badges": badge_id}).sort("badges", -1).limit(10)  # Trier par nombre de badges

    # Chercher les données du badge
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    embed = discord.Embed(
        title=f"🏅 Classement des utilisateurs ayant le badge **{badge['title']}**",
        description=f"Voici les 10 utilisateurs ayant le badge {badge['emoji']}",
        color=discord.Color.gold()
    )

    # Utilisez count_documents pour obtenir le nombre de documents correspondants
    if collection20.count_documents({"badges": badge_id}) == 0:
        embed.add_field(name="Aucun utilisateur", value="Aucun utilisateur ne possède ce badge.", inline=False)
    else:
        # Ajouter les utilisateurs au classement
        for idx, user_data in enumerate(leaderboard, start=1):
            user = await bot.fetch_user(user_data["user_id"])
            badge_count = len(user_data.get("badges", []))  # Compter le nombre total de badges
            embed.add_field(name=f"{idx}. {user.display_name}", value=f"{badge_count} badges", inline=False)

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour filtrer par badge dans le leaderboard
@app_commands.autocomplete(badge_id=True)
async def badge_autocomplete_by_name(interaction: discord.Interaction, current: str):
    results = collection19.find(
        {"title": {"$regex": f"^{current}", "$options": "i"}}  # Autocomplétion par titre de badge
    ).limit(20)

    choices = []
    for badge in results:
        choices.append(app_commands.Choice(name=f"{badge['title']} {badge['emoji']} (ID: {badge['id']})", value=badge["id"]))

    return choices

@bot.tree.command(name="badge-take", description="(Admin) Retire un badge d'un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui retirer le badge",
    badge_id="ID du badge à retirer"
)
async def badge_take(interaction: discord.Interaction, member: discord.Member, badge_id: int):
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    user_data = collection20.find_one({"user_id": member.id})
    if not user_data or badge_id not in user_data.get("badges", []):
        embed = discord.Embed(
            title="❌ Badge non possédé",
            description=f"{member.mention} ne possède pas ce badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    collection20.update_one(
        {"user_id": member.id},
        {"$pull": {"badges": badge_id}}
    )

    embed = discord.Embed(
        title="🧼 Badge retiré",
        description=f"Le badge **{badge['title']}** {badge['emoji']} a été retiré à {member.mention}.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset-badge", description="Réinitialise ou supprime un badge de la boutique")
@app_commands.describe(badge_id="ID du badge à réinitialiser ou supprimer")
async def reset_badge(interaction: discord.Interaction, badge_id: int):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    badge = collection19.find_one({"id": badge_id})
    if not badge:
        return await interaction.response.send_message(f"❌ Aucun badge trouvé avec l'ID {badge_id}.", ephemeral=True)

    # Supprime le badge de la boutique
    collection19.delete_one({"id": badge_id})

    return await interaction.response.send_message(
        f"✅ Le badge **{badge['title']}** {badge.get('emoji', '')} a été supprimé de la boutique.", ephemeral=True
    )

#------------------------------------------------ Connexion Season

def get_start_date(guild_id):
    data = collection22.find_one({"guild_id": guild_id})
    if not data or "start_date" not in data:
        return None
    return datetime.fromisoformat(data["start_date"])


@bot.tree.command(name="start-rewards", description="Définit la date de début des rewards (réservé à ISEY)")
async def start_rewards(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("❌ Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
        return

    guild_id = interaction.guild.id
    now = datetime.utcnow()
    timestamp = int(now.timestamp())

    existing = collection22.find_one({"guild_id": guild_id})

    if existing:
        # Cas où un cycle est en cours
        if 'end_timestamp' not in existing:
            await interaction.response.send_message(
                f"⚠️ Un cycle de rewards est déjà en cours depuis le <t:{int(existing['start_timestamp'])}:F>.",
                ephemeral=True
            )
            return

        # Cas où le cycle précédent est terminé → on en relance un nouveau
        collection22.update_one(
            {"guild_id": guild_id},
            {"$set": {
                "start_date": now.isoformat(),
                "start_timestamp": timestamp
            }, "$unset": {
                "end_date": "",
                "end_timestamp": ""
            }}
        )
        await interaction.response.send_message(
            f"🔁 Nouveau cycle de rewards lancé ! Début : <t:{timestamp}:F>",
            ephemeral=True
        )
        return

    # Cas où aucun document n’existe encore → premier lancement
    collection22.insert_one({
        "guild_id": guild_id,
        "start_date": now.isoformat(),
        "start_timestamp": timestamp
    })

    await interaction.response.send_message(
        f"✅ Le système de rewards a bien été lancé pour la première fois ! Début : <t:{timestamp}:F>",
        ephemeral=True
    )

# === COMMANDE SLASH /rewards ===
@bot.tree.command(name="rewards", description="Récupère ta récompense quotidienne")
async def rewards(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    # Vérifier la date de début des récompenses
    start_date = get_start_date(guild_id)
    if not start_date:
        await interaction.response.send_message("Le système de récompenses n'est pas encore configuré.", ephemeral=True)
        return

    # Calculer le nombre de jours écoulés depuis le début
    days_elapsed = (datetime.utcnow() - start_date).days + 1
    if days_elapsed > 7:
        await interaction.response.send_message("La période de récompenses est terminée.", ephemeral=True)
        return

    # Récupérer les données de l'utilisateur
    user_data = collection23.find_one({"guild_id": guild_id, "user_id": user_id})
    received = user_data.get("rewards_received", {}) if user_data else {}

    # Vérifier si la récompense d’aujourd’hui a déjà été récupérée
    if str(days_elapsed) in received:
        await interaction.response.send_message("Tu as déjà récupéré ta récompense aujourd'hui.", ephemeral=True)
        return

    # Vérifier si une récompense a été manquée
    for i in range(1, days_elapsed):
        if str(i) not in received:
            await interaction.response.send_message("Tu as manqué un jour. Tu ne peux plus récupérer les récompenses.", ephemeral=True)
            return

    # Si toutes les vérifications sont passées, donner la récompense
    await give_reward(interaction, days_elapsed)

# === Fonction pour donner la récompense ===
async def give_reward(interaction: discord.Interaction, day: int):
    reward = daily_rewards.get(day)
    if not reward:
        await interaction.response.send_message("Aucune récompense disponible pour ce jour.", ephemeral=True)
        return

    coins = reward.get("coins", 0)
    badge = reward.get("badge")
    item = reward.get("item")
    random_items = reward.get("random_items")

    # Si random_items est défini, choisir un item au hasard en fonction des chances
    if random_items and isinstance(random_items, list):
        total_chance = sum(entry["chance"] for entry in random_items)  # Somme des chances
        roll = random.uniform(0, total_chance)  # Tirage au sort entre 0 et la somme totale des chances
        cumulative_chance = 0
        for entry in random_items:
            cumulative_chance += entry["chance"]
            if roll <= cumulative_chance:  # Si le tirage est inférieur ou égal à la chance cumulative
                item = entry["id"]  # Choisir cet item
                break

    # === Récompense enregistrée (collection23) ===
    user_data = collection23.find_one({"guild_id": interaction.guild.id, "user_id": interaction.user.id})
    if not user_data:
        user_data = {"guild_id": interaction.guild.id, "user_id": interaction.user.id, "rewards_received": {}}

    user_data["rewards_received"][str(day)] = reward
    collection23.update_one(
        {"guild_id": interaction.guild.id, "user_id": interaction.user.id},
        {"$set": user_data},
        upsert=True
    )

    # === Coins (collection économie) ===
    eco_data = collection.find_one({"guild_id": interaction.guild.id, "user_id": interaction.user.id})
    if not eco_data:
        collection.insert_one({
            "guild_id": interaction.guild.id,
            "user_id": interaction.user.id,
            "cash": coins,
            "bank": 0
        })
    else:
        collection.update_one(
            {"guild_id": interaction.guild.id, "user_id": interaction.user.id},
            {"$inc": {"cash": coins}}
        )

    # === Badge (collection20) ===
    if badge:
        badge_data = collection20.find_one({"user_id": interaction.user.id})
        if not badge_data:
            collection20.insert_one({"user_id": interaction.user.id, "badges": [badge]})
        elif badge not in badge_data.get("badges", []):
            collection20.update_one(
                {"user_id": interaction.user.id},
                {"$push": {"badges": badge}}
            )

    # === Item (collection17) ===
    item_config = None
    if item:
        item_config = collection18.find_one({"id": item})
        if item_config:
            collection17.insert_one({
                "guild_id": interaction.guild.id,
                "user_id": interaction.user.id,
                "item_id": item,
                "item_name": item_config.get("title", "Nom inconnu"),
                "emoji": item_config.get("emoji", "")
            })

    # === Embed de récompense ===
    days_received = len(user_data["rewards_received"])
    total_days = 7
    embed = discord.Embed(
        title="🎁 Récompense de la journée",
        description=f"Voici ta récompense pour le jour {day} !",
        color=discord.Color.green()
    )
    embed.add_field(name="Coins", value=f"{coins} <:ecoEther:1341862366249357374>", inline=False)
    if badge:
        embed.add_field(name="Badge", value=f"Badge ID {badge}", inline=False)
    if item and item_config:
        embed.add_field(name="Item", value=f"{item_config.get('title', 'Nom inconnu')} {item_config.get('emoji', '')} (ID: {item})", inline=False)
    embed.set_image(url=reward["image_url"])

    progress = "█" * days_received + "░" * (total_days - days_received)
    embed.add_field(name="Progression", value=f"{progress} ({days_received}/{total_days})", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="zero-rewards", description="Réinitialise les récompenses de tous les utilisateurs")
async def zero_rewards(interaction: discord.Interaction):
    # Vérifier si l'utilisateur est ISEY_ID
    if interaction.user.id != 792755123587645461:
        await interaction.response.send_message("Tu n'as pas l'autorisation d'utiliser cette commande.", ephemeral=True)
        return
    
    # Parcourir tous les utilisateurs dans la collection de récompenses
    all_users = collection23.find({"rewards_received": {"$exists": True}})
    
    updated_count = 0
    for user_data in all_users:
        # Réinitialiser les récompenses de l'utilisateur
        collection23.update_one(
            {"guild_id": user_data["guild_id"], "user_id": user_data["user_id"]},
            {"$set": {"rewards_received": {}}}
        )
        updated_count += 1

    # Répondre avec un message de confirmation
    await interaction.response.send_message(f"Les récompenses ont été réinitialisées pour {updated_count} utilisateur(s).", ephemeral=True)

@bot.tree.command(name="end-rewards", description="Définit la date de fin des rewards (réservé à ISEY)")
async def end_rewards(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("❌ Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
        return

    guild_id = interaction.guild.id
    existing = collection22.find_one({"guild_id": guild_id})

    if not existing:
        await interaction.response.send_message("⚠️ Aucun début de rewards trouvé. Utilise d'abord `/start-rewards`.", ephemeral=True)
        return

    if 'end_timestamp' in existing:
        await interaction.response.send_message(
            f"⚠️ Les rewards ont déjà été terminés le <t:{int(existing['end_timestamp'])}:F>.",
            ephemeral=True
        )
        return

    now = datetime.utcnow()
    timestamp = int(now.timestamp())

    collection22.update_one(
        {"guild_id": guild_id},
        {"$set": {
            "end_date": now.isoformat(),
            "end_timestamp": timestamp
        }}
    )

    updated = collection22.find_one({"guild_id": guild_id})

    await interaction.response.send_message(
        f"✅ Les rewards ont été clôturés !\nPériode : du <t:{updated['start_timestamp']}:F> au <t:{updated['end_timestamp']}:F>",
        ephemeral=True
    )


#------------------------------------- Quetes

# Fonction pour insérer des quêtes de départ dans la base de données
def insert_quetes_into_db():
    # Quêtes à insérer au démarrage
    quetes_debut = [
        {"id": 1, "nom": "Quête de début", "description": "Commencez votre aventure !", "emoji": "🌟", "recompense": "100"},
        {"id": 2, "nom": "Quête de récolte", "description": "Récoltez des ressources.", "emoji": "🌾", "recompense": "200"}
    ]
    
    for quete in quetes_debut:
        # Vérifier si la quête existe déjà dans la base de données
        if not collection32.find_one({"id": quete["id"]}):
            collection32.insert_one(quete)

@bot.tree.command(name="add-quete", description="Ajoute une nouvelle quête.")
@app_commands.describe(
    quest_id="L'ID unique de la quête",
    nom="Nom de la quête",
    description="Description de la quête",
    reward_item_id="ID de l'item en récompense (doit exister dans la boutique)",
    reward_coins="Montant de pièces en récompense"
)
async def add_quete(interaction: discord.Interaction, quest_id: int, nom: str, description: str, reward_item_id: int, reward_coins: int):
    if interaction.user.id != 792755123587645461:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    # Vérifie que l'item existe
    item = collection16.find_one({"id": reward_item_id})
    if not item:
        return await interaction.response.send_message("❌ L'item spécifié n'existe pas dans la boutique.", ephemeral=True)

    existing = collection32.find_one({"id": quest_id})
    if existing:
        return await interaction.response.send_message("❌ Une quête avec cet ID existe déjà.", ephemeral=True)

    quest = {
        "id": quest_id,
        "nom": nom,
        "description": description,
        "reward_item_id": reward_item_id,
        "reward_coins": reward_coins
    }

    collection32.insert_one(quest)
    await interaction.response.send_message(f"✅ Quête **{nom}** ajoutée avec succès !", ephemeral=True)

@bot.tree.command(name="quetes", description="Affiche la liste des quêtes disponibles")
async def quetes(interaction: discord.Interaction):
    quests = list(collection32.find({}))

    if not quests:
        return await interaction.response.send_message("❌ Aucune quête enregistrée.", ephemeral=True)

    # Créez l'embed avec l'utilisateur comme auteur
    embed = discord.Embed(title=f"Quêtes disponibles", color=discord.Color.blue())
    
    # Ajout de la photo de profil de l'utilisateur
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    # Ajout de l'emoji personnalisé en haut à droite
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1364316821196640306.png")  # Utilisation du lien direct pour l'emoji personnalisé

    for quest in quests:
        item = collection16.find_one({"id": quest["reward_item_id"]})
        item_name = item["title"] if item else "Inconnu"
        item_emoji = item["emoji"] if item else ""

        # Si la quête a été réalisée, on la barre et on affiche la personne qui l'a complétée
        if 'completed_by' in quest:
            completed_by = quest['completed_by']
            quest_name = f"~~{quest['nom']}~~"
            quest_value = f"{quest['description']}\n**Récompense**: {item_name} {item_emoji} + {quest['reward_coins']} <:ecoEther:1341862366249357374>\n**Complétée par**: {completed_by}"
        else:
            quest_name = f"🔹 {quest['nom']} (ID: {quest['id']})"
            quest_value = f"{quest['description']}\n**Récompense**: {item_name} {item_emoji} + {quest['reward_coins']} <:ecoEther:1341862366249357374>"

        embed.add_field(
            name=quest_name,
            value=quest_value,
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quete-faite", description="Valide une quête et donne les récompenses à un utilisateur.")
@app_commands.describe(quest_id="ID de la quête", user="Utilisateur à récompenser")
async def quete_faite(interaction: discord.Interaction, quest_id: int, user: discord.User):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    quest = collection32.find_one({"id": quest_id})
    if not quest:
        return await interaction.response.send_message("❌ Quête introuvable.", ephemeral=True)

    # Ajouter item dans l'inventaire
    collection17.insert_one({
        "guild_id": interaction.guild.id,
        "user_id": user.id,
        "item_id": quest["reward_item_id"],
        "item_name": collection16.find_one({"id": quest["reward_item_id"]})["title"],
        "emoji": collection16.find_one({"id": quest["reward_item_id"]})["emoji"]
    })

    # Ajouter des coins
    user_data = collection.find_one({"guild_id": interaction.guild.id, "user_id": user.id})
    if not user_data:
        user_data = {"guild_id": interaction.guild.id, "user_id": user.id, "cash": 0, "bank": 0}
        collection.insert_one(user_data)

    new_cash = user_data["cash"] + quest["reward_coins"]
    collection.update_one(
        {"guild_id": interaction.guild.id, "user_id": user.id},
        {"$set": {"cash": new_cash}}
    )

    # Marquer la quête comme complétée par l'utilisateur
    collection32.update_one(
        {"id": quest_id},
        {"$set": {"completed_by": user.name}}
    )

    await interaction.response.send_message(
        f"✅ Récompenses de la quête **{quest['nom']}** données à {user.mention} !",
        ephemeral=True
    )

@bot.tree.command(name="reset-quetes", description="Supprime toutes les quêtes (ADMIN)")
async def reset_quetes(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("Tu n'as pas l'autorisation d'utiliser cette commande.", ephemeral=True)
        return

    result = collection32.delete_many({})
    await interaction.response.send_message(f"🧹 Collection `ether_quetes` reset avec succès. {result.deleted_count} quêtes supprimées.")

from discord import Embed
import matplotlib.pyplot as plt
import numpy as np
import io
import discord

# Fonction d'union des plages (par exemple, union de [6;7] et [11;19])
def union_intervals(intervals):
    # Tri des intervalles par le début de chaque intervalle
    intervals.sort(key=lambda x: x[0])
    merged = []
    
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged

# Fonction d'intersection des plages
def intersection_intervals(intervals):
    # Intersection de toutes les plages disponibles
    min_end = min(interval[1] for interval in intervals)
    max_start = max(interval[0] for interval in intervals)
    
    if max_start <= min_end:
        return [(max_start, min_end)]  # Renvoie l'intersection
    return []

import discord
from discord import Embed
import matplotlib.pyplot as plt
import io

@bot.tree.command(name="id-items", description="📚 Affiche les IDs d'items utilisés et les plages libres")
async def id_items(interaction: discord.Interaction):
    # Récupérer uniquement les documents qui possèdent un champ 'id'
    all_items = list(collection16.find({"id": {"$exists": True}}, {"id": 1, "_id": 0}))
    used_ids = sorted(item["id"] for item in all_items)

    # IDs totaux possibles
    total_ids = list(range(1, 1001))

    # Calcul des IDs libres
    free_ids = [i for i in total_ids if i not in used_ids]

    # Génération des plages libres
    free_intervals = []
    current_start = None

    for i in total_ids:
        if i in free_ids:
            if current_start is None:
                current_start = i
        else:
            if current_start is not None:
                free_intervals.append((current_start, i - 1))
                current_start = None
    if current_start is not None:
        free_intervals.append((current_start, 1000))

    # Graphique de l'utilisation
    usage_percentage = len(used_ids) / len(total_ids) * 100
    free_percentage = 100 - usage_percentage

    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Utilisés', 'Libres']
    sizes = [usage_percentage, free_percentage]
    colors = ['#FF6B6B', '#4ECDC4']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plt.close()

    # Création de l'embed Discord
    embed = Embed(
        title="📚 Analyse des IDs d'Items",
        description="Voici l'état actuel des IDs utilisés et disponibles.",
        color=discord.Color.blurple()
    )

    # Gestion du champ des IDs utilisés
    ids_used_text = ', '.join(map(str, used_ids))
    if len(ids_used_text) > 1024:
        ids_used_text = ids_used_text[:1020] + "..."

    embed.add_field(
        name="🛠️ IDs Utilisés",
        value=f"`{len(used_ids)}` IDs utilisés\n`{ids_used_text}`",
        inline=False
    )

    # Gestion du champ des plages d'IDs libres
    free_intervals_text = "\n".join(
        f"`[{start} ➔ {end}]`" if start != end else f"`[{start}]`" for start, end in free_intervals
    )
    if len(free_intervals_text) > 1024:
        free_intervals_text = free_intervals_text[:1020] + "..."

    embed.add_field(
        name="📖 Plages d'IDs Libres",
        value=free_intervals_text,
        inline=False
    )

    embed.add_field(
        name="📊 Statistiques",
        value=f"**Total IDs :** `{len(total_ids)}`\n"
              f"**Utilisés :** `{len(used_ids)} ({usage_percentage:.2f}%)`\n"
              f"**Libres :** `{len(free_ids)} ({free_percentage:.2f}%)`",
        inline=False
    )

    embed.set_image(url="attachment://usage_graph.png")
    embed.set_footer(text="Etherya • Visualisation des IDs", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

    file = discord.File(buf, filename="usage_graph.png")
    await interaction.response.send_message(embed=embed, file=file)

import random
import discord
from discord import Embed, ButtonStyle
from discord.ui import View, Button

@bot.tree.command(name="id-random", description="🎲 Tire un ID libre automatiquement parmi ceux disponibles en boutique")
async def id_random(interaction: discord.Interaction):
    # Aller chercher tous les IDs utilisés directement depuis MongoDB
    used_ids = [doc["id"] for doc in collection16.find({}, {"id": 1}) if "id" in doc]

    # IDs possibles de 1 à 1000 (par exemple)
    total_ids = list(range(1, 1001))

    # IDs libres = ceux pas utilisés
    free_ids = [i for i in total_ids if i not in used_ids]

    # Fonction pour tirer un ID libre au hasard
    def pick_random_id():
        return random.choice(free_ids) if free_ids else None

    random_id = pick_random_id()

    if random_id is None:
        await interaction.response.send_message("❌ Aucun ID disponible.", ephemeral=True)
        return

    # Embed de réponse
    embed = Embed(
        title="🎲 ID Libre Tiré",
        description=f"Voici un ID libre :\n\n`{random_id}`",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Clique sur 🔄 pour tirer un autre ID !", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

    # Vue avec bouton Re-roll
    class RandomIDView(View):
        def __init__(self):
            super().__init__(timeout=30)

        @discord.ui.button(label="Re-roll 🔄", style=ButtonStyle.primary)
        async def reroll(self, interaction_button: discord.Interaction, button: Button):
            new_id = pick_random_id()
            if new_id is None:
                await interaction_button.response.edit_message(content="❌ Aucun ID disponible.", embed=None, view=None)
                return

            new_embed = Embed(
                title="🎲 ID Libre Tiré",
                description=f"Voici un nouvel ID libre :\n\n`{new_id}`",
                color=discord.Color.gold()
            )
            new_embed.set_footer(text="Clique sur 🔄 pour tirer un autre ID !", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

            await interaction_button.response.edit_message(embed=new_embed)

    await interaction.response.send_message(embed=embed, view=RandomIDView())

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
