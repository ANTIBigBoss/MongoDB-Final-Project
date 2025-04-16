// 1. INSERTONE: Insert the sample document for ANTIBigBoss.
db.players.insertOne({
    player_id: "ANTIBigBoss",
    username: "ANTIBigBoss",
    stats: {
      rounds: 7722,
      wins: 2853,
      score: 196337,
      time_played_days: 27,
      kills: {
        headshot: 13025,
        lock_on: 8982,
        other: 9765,
        all: 31772
      },
      deaths: {
        headshot: 13037,
        lock_on: 1601,
        other: 6208,
        all: 20846
      },
      stuns: {
        headshot: 1237,
        lock_on: 1512,
        other: 3952,
        all: 6701
      },
      stuns_received: {
        headshot: 1442,
        lock_on: 197,
        other: 2327,
        all: 3966
      },
      consecutive_kills: 16,
      consecutive_deaths: 10,
      consecutive_headshots: 11,
      suicides: 239,
      friendly_kills: 138,
      friendly_stuns: 19,
      times_stunned: 3966,
      cqc_attacks_given: 3909,
      cqc_attacks_taken: 2157,
      rolls: 38954,
      salutes: 905,
      catapult_uses: 40,
      bases_captured: 378,
      radio_uses: 110438,
      chat_uses: 5408,
      knife_kills: 1082,
      knife_stuns: 1098
    },
    login_info: {
      last_login: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
      login_count: 500,
      ip_address: "192.168.1.69"
    },
    hardware_info: {
      cpu: "Intel i7",
      gpu: "NVIDIA GTX 1070",
      os: "Windows 10",
      ram: 16
    },
    profile: "Veteran player with extensive battle experience.",
    created_at: new Date(),
    animal_rank: null
  });

  
  
  // 2. INSERTMANY: Insert additional sample player documents.
  db.players.insertMany([
    {
      player_id: "Player001",
      username: "ShadowNinja",
      stats: { rounds: 5000, wins: 2300, score: 150000, time_played_days: 15, kills: { all: 21000 }, deaths: { all: 15000 }, stuns: { all: 3000 }, stuns_received: { all: 2500 } },
      login_info: { last_login: new Date(), login_count: 350, ip_address: "192.168.1.101" },
      hardware_info: { cpu: "Intel i5", gpu: "NVIDIA GTX 1060", os: "Windows 10", ram: 8 },
      profile: "Fast and stealthy.",
      created_at: new Date(),
      animal_rank: null
    },
    {
      player_id: "Player002",
      username: "StealthMaster",
      stats: { rounds: 6000, wins: 2800, score: 170000, time_played_days: 20, kills: { all: 25000 }, deaths: { all: 18000 }, stuns: { all: 3500 }, stuns_received: { all: 2700 } },
      login_info: { last_login: new Date(), login_count: 400, ip_address: "192.168.1.102" },
      hardware_info: { cpu: "AMD Ryzen 7", gpu: "NVIDIA GTX 1080", os: "Windows 10", ram: 16 },
      profile: "Expert in covert operations.",
      created_at: new Date(),
      animal_rank: null
    }
  ]);

  
  // 3. FIND: Retrieve the document for ANTIBigBoss.
  db.players.find({ player_id: "ANTIBigBoss" });
  
  // 4. FIND (Projection): Retrieve only the username, rounds, and animal_rank fields for ANTIBigBoss.
  db.players.find(
    { player_id: "ANTIBigBoss" },
    { username: 1, "stats.rounds": 1, animal_rank: 1, _id: 0 }
  );
  

  // 5. UPDATEONE: Update the animal_rank field for ANTIBigBoss (for example, set rank to "Fox").
  db.players.updateOne(
    { player_id: "ANTIBigBoss" },
    { $set: { animal_rank: "Fox" } }
  );
  
  // 6. UPDATEMANY: Increase the login_count by 1 for all players with a login_count over 100.
  db.players.updateMany(
    { "login_info.login_count": { $gte: 100 } },
    { $inc: { "login_info.login_count": 1 } }
  );
  
  // 7. DELETEONE: Remove one document with a specific player_id (e.g., "TestPlayer").
  db.players.deleteOne({ player_id: "TestPlayer" });
  
  // 8. DELETEMANY: Remove all documents created before January 1, 2025.
  db.players.deleteMany({ created_at: { $lt: new Date("2025-01-01") } });

  // 9. AGGREGATION: Calculate the average score of all players.
  db.players.aggregate([
    { $group: { _id: null, avgScore: { $avg: "$stats.score" } } }
  ]);
  
  // 10. AGGREGATION with SORT: Retrieve the top 5 players sorted by score in descending order.
  db.players.aggregate([
    { $sort: { "stats.score": -1 } },
    { $limit: 5 },
    { $project: { player_id: 1, username: 1, "stats.score": 1, _id: 0 } }
  ]);
  
  // 11. SORTING: Return all players sorted by time_played_days (highest to lowest).
  db.players.find({}, { username: 1, "stats.time_played_days": 1, _id: 0 })
           .sort({ "stats.time_played_days": -1 });
  
  // 12. INDEXING: Create an index on the username field for faster queries.
  db.players.createIndex({ username: 1 });
    db.players.createIndex({ profile: "text" });
  
  // 13. TEXT SEARCH: Search for players whose profile contains the keyword "veteran".
  db.players.find({ $text: { $search: "veteran" } });
  
  // 14. REGEX QUERY: Find players whose username starts with "ANTI" (case-insensitive).
  db.players.find({ username: { $regex: /^ANTI/, $options: "i" } });

  // 15. TRANSACTION QUERY: Perform multiple operations atomically.
  var session = db.getMongo().startSession();
  session.startTransaction();
  try {
    var dbSession = session.getDatabase("metal_gear_online");
    
    dbSession.players.updateOne(
      { player_id: "ANTIBigBoss" },
      { $set: { "stats.score": 200000 } },
      { session: session }
    );
    
    dbSession.players.insertOne(
      {
        player_id: "TempPlayer",
        username: "TempPlayer",
        stats: { rounds: 100, wins: 50, score: 10000, time_played_days: 5 },
        login_info: { last_login: new Date(), login_count: 10, ip_address: "127.0.0.1" },
        hardware_info: { cpu: "Intel i3", gpu: "Integrated", os: "Linux", ram: 4 },
        profile: "Temporary test record.",
        created_at: new Date(),
        animal_rank: null
      },
      { session: session }
    );
    
    session.commitTransaction();
    print("Transaction committed successfully.");
  } catch (error) {
    session.abortTransaction();
    print("Transaction aborted due to error: " + error);
  } finally {
    session.endSession();
  }