from pathlib import Path
import pandas as pd
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)

class WPLDataCleaner:
    def __init__(self, input_path: str = None):
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        
        # Use the specific file name with spaces
        self.input_file = input_path or self.raw_path / 'Wpl 2023-2024.csv'
        
        # Ensure processed directory exists
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def clean_data(self):
        """Main data cleaning method"""
        logger.info(f"Starting data cleaning process...")
        logger.info(f"Reading data from: {self.input_file}")
        
        try:
            # Check if file exists
            if not self.input_file.exists():
                raise FileNotFoundError(f"Could not find file: {self.input_file}")
            
            # Read the CSV file
            df = pd.read_csv(self.input_file)
            logger.info(f"Successfully read {len(df)} rows of data")
            
            # Clean column names
            df.columns = df.columns.str.lower().str.strip()
            
            # Basic cleaning steps
            df = self._clean_dates(df)
            df = self._clean_team_names(df)
            df = self._clean_match_details(df)
            df = self._add_calculated_fields(df)
            
            # Save processed data
            output_file = self.processed_path / 'wpl_clean.csv'
            df.to_csv(output_file, index=False)
            logger.info(f"Cleaned data saved to: {output_file}")
            
            # Generate summary
            self._generate_summary(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Error in data cleaning process: {str(e)}")
            raise
    
    def _clean_dates(self, df):
        """Clean and standardize dates"""
        try:
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df
        except Exception as e:
            logger.error(f"Error cleaning dates: {str(e)}")
            raise
    
    def _clean_team_names(self, df):
        """Standardize team names"""
        team_columns = ['team1', 'team2', 'winner', 'toss_winner']
        for col in team_columns:
            if col in df.columns:
                df[col] = df[col].str.strip()
        
        if 'venue' in df.columns:
            df['venue'] = df['venue'].str.strip()
            df['city'] = df['city'].str.strip()
        
        return df
    
    def _clean_match_details(self, df):
        """Clean match-specific details"""
        # Convert winner runs and wickets to numeric
        numeric_cols = ['winner_runs', 'winner_wickets']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Clean match number - handle missing values
        def extract_match_number(x):
            if pd.isna(x):
                return None
            match = re.search(r'(\d+)', str(x))
            return int(match.group(1)) if match else None
        
        df['match_number'] = df['match_number'].apply(extract_match_number)
        
        return df
    
    def _add_calculated_fields(self, df):
        """Add calculated statistics"""
        # Add match margin type
        df['win_type'] = np.where(df['winner_runs'].notna(), 'runs', 
                                 np.where(df['winner_wickets'].notna(), 'wickets', 'unknown'))
        
        # Add margin value
        df['margin'] = np.where(df['win_type'] == 'runs', df['winner_runs'],
                               np.where(df['win_type'] == 'wickets', df['winner_wickets'], np.nan))
        
        # Add home advantage indicator
        df['is_home_win'] = df.apply(lambda x: x['winner'] == x['team1'], axis=1)
        
        # Add toss factor
        df['won_toss_and_match'] = df['winner'] == df['toss_winner']
        
        # Add match outcome details
        df['match_result'] = df.apply(
            lambda x: f"{x['winner']} won by {int(x['margin'])} {x['win_type']}" 
            if pd.notna(x['margin']) else "No result",
            axis=1
        )
        
        return df
    
    def _generate_summary(self, df):
        """Generate and save data summary"""
        summary_file = self.processed_path / 'data_summary.txt'
        
        with open(summary_file, 'w') as f:
            f.write("WPL Data Summary\n")
            f.write("===============\n\n")
            
            f.write(f"Total Matches: {len(df)}\n")
            f.write(f"Season: {df['season'].unique()[0]}\n")
            f.write(f"Date Range: {df['date'].min()} to {df['date'].max()}\n\n")
            
            f.write("Teams Performance:\n")
            f.write("------------------\n")
            teams = set(df['team1'].unique()) | set(df['team2'].unique())
            for team in sorted(teams):
                team_wins = len(df[df['winner'] == team])
                total_matches = len(df[(df['team1'] == team) | (df['team2'] == team)])
                win_rate = (team_wins / total_matches * 100) if total_matches > 0 else 0
                f.write(f"{team}:\n")
                f.write(f"- Matches played: {total_matches}\n")
                f.write(f"- Matches won: {team_wins}\n")
                f.write(f"- Win rate: {win_rate:.1f}%\n\n")
            
            f.write("\nVenue Statistics:\n")
            f.write("----------------\n")
            venue_stats = df.groupby('venue').agg({
                'match_number': 'count',
                'winner_runs': lambda x: x.mean(skipna=True),
                'winner_wickets': lambda x: x.mean(skipna=True)
            }).round(2)
            
            for venue, stats in venue_stats.iterrows():
                f.write(f"{venue}:\n")
                f.write(f"- Matches hosted: {int(stats['match_number'])}\n")
                if not pd.isna(stats['winner_runs']):
                    f.write(f"- Average winning margin (runs): {stats['winner_runs']}\n")
                if not pd.isna(stats['winner_wickets']):
                    f.write(f"- Average winning margin (wickets): {stats['winner_wickets']}\n")
                f.write("\n")
            
            f.write("\nToss Impact:\n")
            f.write("-----------\n")
            toss_wins = len(df[df['won_toss_and_match']])
            toss_win_percentage = (toss_wins / len(df)) * 100
            f.write(f"Teams winning both toss and match: {toss_wins} ({toss_win_percentage:.1f}%)\n")
            
            f.write("\nTop Players:\n")
            f.write("-----------\n")
            pom_counts = df['player_of_match'].value_counts()
            f.write("Player of the Match awards:\n")
            for player, count in pom_counts.head().items():
                f.write(f"- {player}: {count} awards\n")
        
        logger.info(f"Data summary saved to: {summary_file}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Run the cleaner
    cleaner = WPLDataCleaner()
    cleaner.clean_data()