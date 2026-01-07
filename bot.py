import discord
from discord.ext import commands
import json, os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

HISTORY_FILE = "spice_history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def spicerun(ctx, total_melange: int, *players):
    if not players:
        await ctx.send("❌ Provide player names.")
        return

    per_player = total_melange // len(players)
    remainder = total_melange % len(players)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    history = load_history()
    history.append({
        "time": timestamp,
        "total": total_melange,
        "players": list(players),
        "each": per_player,
        "remainder": remainder
    })
    save_history(history)

    msg = f"🟠 **Spice Run Complete** 🟠\n🕒 {timestamp}\n"
    msg += f"Total: {total_melange}\nPlayers:\n"
    for p in players:
        msg += f"- {p}: {per_player}\n"
    if remainder:
        msg += f"\n⚠️ Remainder: {remainder}"

    await ctx.send(msg)

@bot.command()
async def spicehistory(ctx):
    history = load_history()
    if not history:
        await ctx.send("📭 No spice history.")
        return

    msg = "📊 **Recent Spice Runs** 📊\n"
    for run in history[-5:]:
        msg += f"\n{run['time']} — Total {run['total']} | Each {run['each']}"
    await ctx.send(msg)

bot.run(os.getenv("DISCORD_TOKEN"))
