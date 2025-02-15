from sqlalchemy import Column, Integer, String, DateTime, Float, Date
from sqlalchemy.sql import func
from app.db.database import Base

class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    value = Column(Float)
    category = Column(String)
    source = Column(String)
    
    def __repr__(self):
        return f"<DataPoint(id={self.id}, timestamp={self.timestamp}, value={self.value})>"

class WPLMatch(Base):
    __tablename__ = "wpl_matches"

    id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date)
    venue = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    winner = Column(String)
    player_of_match = Column(String)
    team1_score = Column(Integer)
    team1_wickets = Column(Integer)
    team1_overs = Column(Float)
    team2_score = Column(Integer)
    team2_wickets = Column(Integer)
    team2_overs = Column(Float)

class WPLPlayerStats(Base):
    __tablename__ = "wpl_player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String)
    team = Column(String)
    matches = Column(Integer)
    runs = Column(Integer)
    wickets = Column(Integer)
    batting_average = Column(Float)
    bowling_average = Column(Float)
    strike_rate = Column(Float)
    economy_rate = Column(Float)

# Analytics functions
def calculate_team_stats(matches):
    """Calculate team-wise statistics from matches"""
    team_stats = {}
    
    for match in matches:
        # Process team1
        if match.team1 not in team_stats:
            team_stats[match.team1] = {
                'matches': 0,
                'wins': 0,
                'losses': 0,
                'total_runs': 0,
                'total_wickets': 0
            }
        
        # Process team2
        if match.team2 not in team_stats:
            team_stats[match.team2] = {
                'matches': 0,
                'wins': 0,
                'losses': 0,
                'total_runs': 0,
                'total_wickets': 0
            }
        
        # Update match stats
        team_stats[match.team1]['matches'] += 1
        team_stats[match.team2]['matches'] += 1
        
        if match.winner == match.team1:
            team_stats[match.team1]['wins'] += 1
            team_stats[match.team2]['losses'] += 1
        elif match.winner == match.team2:
            team_stats[match.team2]['wins'] += 1
            team_stats[match.team1]['losses'] += 1
            
        # Update runs and wickets
        team_stats[match.team1]['total_runs'] += match.team1_score
        team_stats[match.team1]['total_wickets'] += match.team2_wickets
        team_stats[match.team2]['total_runs'] += match.team2_score
        team_stats[match.team2]['total_wickets'] += match.team1_wickets
    
    return team_stats

def get_top_players(player_stats, category='runs', limit=5):
    """Get top players based on different categories"""
    if category == 'runs':
        return sorted(player_stats, key=lambda x: x.runs, reverse=True)[:limit]
    elif category == 'wickets':
        return sorted(player_stats, key=lambda x: x.wickets, reverse=True)[:limit]
    elif category == 'batting_average':
        return sorted(player_stats, key=lambda x: x.batting_average or 0, reverse=True)[:limit]
    elif category == 'bowling_average':
        return sorted(player_stats, key=lambda x: x.bowling_average or float('inf'))[:limit]
    return []