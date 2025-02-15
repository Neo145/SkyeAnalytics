from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
from app.db.database import get_db
from app.db.models import WPLMatch, WPLPlayerStats
from app.db.models import calculate_team_stats, get_top_players

router = APIRouter(prefix="/wpl", tags=["wpl"])

@router.post("/import-data")
async def import_wpl_data(db: Session = Depends(get_db)):
    try:
        # Read CSV file
        df = pd.read_csv("wpl_2023_2024.csv")
        
        # Process matches data
        for _, row in df.iterrows():
            match = WPLMatch(
                match_date=pd.to_datetime(row['date']).date(),
                venue=row['venue'],
                team1=row['team1'],
                team2=row['team2'],
                winner=row['winner'],
                player_of_match=row['player_of_match'],
                team1_score=row['team1_score'],
                team1_wickets=row['team1_wickets'],
                team1_overs=row['team1_overs'],
                team2_score=row['team2_score'],
                team2_wickets=row['team2_wickets'],
                team2_overs=row['team2_overs']
            )
            db.add(match)
        
        db.commit()
        return {"status": "success", "message": "Data imported successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matches")
async def get_matches(db: Session = Depends(get_db)):
    matches = db.query(WPLMatch).all()
    return matches

@router.get("/team-stats")
async def get_team_statistics(db: Session = Depends(get_db)):
    matches = db.query(WPLMatch).all()
    team_stats = calculate_team_stats(matches)
    return team_stats

@router.get("/top-players/{category}")
async def get_top_players_route(
    category: str,
    limit: Optional[int] = 5,
    db: Session = Depends(get_db)
):
    players = db.query(WPLPlayerStats).all()
    top_players = get_top_players(players, category, limit)
    return top_players

@router.get("/match-analysis")
async def get_match_analysis(db: Session = Depends(get_db)):
    matches = db.query(WPLMatch).all()
    
    analysis = {
        "total_matches": len(matches),
        "average_first_innings_score": sum(m.team1_score for m in matches) / len(matches),
        "average_second_innings_score": sum(m.team2_score for m in matches) / len(matches),
        "venues": list(set(m.venue for m in matches)),
        "highest_score": max(max(m.team1_score, m.team2_score) for m in matches),
        "players_of_match": list(set(m.player_of_match for m in matches))
    }
    
    return analysis