import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from datetime import datetime
import json

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs1")
db = client["FinalAssignment"]
players_col = db["players"]

def load_players():
    players = list(players_col.find({}, {"player_id": 1, "username": 1, "_id": 0}))
    player_list.delete(0, tk.END)
    for p in players:
        player_list.insert(tk.END, p["player_id"])

def show_player_details(event):
    selection = player_list.curselection()
    if selection:
        pid = player_list.get(selection[0])
        player = players_col.find_one({"player_id": pid})
        details_text.delete("1.0", tk.END)
        details_text.insert(tk.END, json.dumps(player, indent=2, default=str))

def edit_player():
    selection = player_list.curselection()
    if not selection:
        return
    pid = player_list.get(selection[0])
    player = players_col.find_one({"player_id": pid})
    edit_win = tk.Toplevel(root)
    edit_win.title(f"Edit {pid}")
    
    labels = [
        ("Username", "username"),
        ("Profile", "profile"),
        ("Rounds", "rounds"),
        ("Wins", "wins"),
        ("Score", "score"),
        ("Time Played (days)", "time_played_days"),
        ("Kills (all)", "kills_all"),
        ("Deaths (all)", "deaths_all"),
        ("Stuns (all)", "stuns_all"),
        ("Stuns Received (all)", "stuns_received_all")
    ]
    entries = {}
    for i, (lab, key) in enumerate(labels):
        tk.Label(edit_win, text=lab + ":").grid(row=i, column=0, padx=5, pady=2, sticky="w")
        ent = tk.Entry(edit_win, width=40)
        ent.grid(row=i, column=1, padx=5, pady=2)
        entries[key] = ent

    entries["username"].insert(0, player.get("username", ""))
    entries["profile"].insert(0, player.get("profile", ""))
    stats = player.get("stats", {})
    entries["rounds"].insert(0, stats.get("rounds", ""))
    entries["wins"].insert(0, stats.get("wins", ""))
    entries["score"].insert(0, stats.get("score", ""))
    entries["time_played_days"].insert(0, stats.get("time_played_days", ""))
    entries["kills_all"].insert(0, stats.get("kills", {}).get("all", ""))
    entries["deaths_all"].insert(0, stats.get("deaths", {}).get("all", ""))
    entries["stuns_all"].insert(0, stats.get("stuns", {}).get("all", ""))
    entries["stuns_received_all"].insert(0, stats.get("stuns_received", {}).get("all", ""))

    def save_edits():
        try:
            new_username = entries["username"].get().strip()
            new_profile = entries["profile"].get().strip()
            new_rounds = int(entries["rounds"].get().strip())
            new_wins = int(entries["wins"].get().strip())
            new_score = int(entries["score"].get().strip())
            new_time = int(entries["time_played_days"].get().strip())
            new_kills = int(entries["kills_all"].get().strip())
            new_deaths = int(entries["deaths_all"].get().strip())
            new_stuns = int(entries["stuns_all"].get().strip())
            new_stuns_recv = int(entries["stuns_received_all"].get().strip())
            new_stats = {
                "rounds": new_rounds,
                "wins": new_wins,
                "score": new_score,
                "time_played_days": new_time,
                "kills": {"all": new_kills},
                "deaths": {"all": new_deaths},
                "stuns": {"all": new_stuns},
                "stuns_received": {"all": new_stuns_recv}
            }
            players_col.update_one({"player_id": pid}, {"$set": {"username": new_username, "profile": new_profile, "stats": new_stats}})
            messagebox.showinfo("Saved", f"Changes saved for {pid}")
            edit_win.destroy()
            load_players()
            show_player_details(None)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(edit_win, text="Save", command=save_edits).grid(row=len(labels), column=0, columnspan=2, pady=5)
    edit_win.grab_set()

def add_player():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Player")
    fields = {}
    labels = [
        ("Player ID", "player_id"),
        ("Username", "username"),
        ("Profile", "profile"),
        ("Rounds", "rounds"),
        ("Wins", "wins"),
        ("Score", "score"),
        ("Time Played (days)", "time_played_days"),
        ("Kills (all)", "kills_all"),
        ("Deaths (all)", "deaths_all"),
        ("Stuns (all)", "stuns_all"),
        ("Stuns Received (all)", "stuns_received_all")
    ]
    for i, (lab, key) in enumerate(labels):
        tk.Label(add_win, text=lab + ":").grid(row=i, column=0, padx=5, pady=2, sticky="w")
        ent = tk.Entry(add_win, width=40)
        ent.grid(row=i, column=1, padx=5, pady=2)
        fields[key] = ent

    def submit_player():
        try:
            pid = fields["player_id"].get().strip()
            username = fields["username"].get().strip()
            profile = fields["profile"].get().strip()
            rounds = int(fields["rounds"].get().strip())
            wins = int(fields["wins"].get().strip())
            score = int(fields["score"].get().strip())
            tpd = int(fields["time_played_days"].get().strip())
            kills_all = int(fields["kills_all"].get().strip())
            deaths_all = int(fields["deaths_all"].get().strip())
            stuns_all = int(fields["stuns_all"].get().strip())
            stuns_received_all = int(fields["stuns_received_all"].get().strip())
            stats = {
                "rounds": rounds,
                "wins": wins,
                "score": score,
                "time_played_days": tpd,
                "kills": {"all": kills_all},
                "deaths": {"all": deaths_all},
                "stuns": {"all": stuns_all},
                "stuns_received": {"all": stuns_received_all}
            }
            new_doc = {
                "player_id": pid,
                "username": username,
                "stats": stats,
                "login_info": {"last_login": datetime.utcnow(), "login_count": 0, "ip_address": ""},
                "hardware_info": {},
                "profile": profile,
                "created_at": datetime.utcnow(),
                "animal_rank": ""
            }
            players_col.insert_one(new_doc)
            messagebox.showinfo("Success", f"Player {pid} added.")
            add_win.destroy()
            load_players()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(add_win, text="Add Player", command=submit_player).grid(row=len(labels), column=0, columnspan=2, pady=5)
    add_win.grab_set()

root = tk.Tk()
root.title("Player Editor")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
player_list = tk.Listbox(left_frame, width=30)
player_list.pack(fill=tk.Y)
player_list.bind("<<ListboxSelect>>", show_player_details)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
details_text = tk.Text(right_frame, width=70, height=25)
details_text.pack(pady=5)

btn_frame = tk.Frame(right_frame)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Edit Player", command=edit_player).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add Player", command=add_player).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Refresh List", command=load_players).grid(row=0, column=2, padx=5)

load_players()
root.mainloop()
