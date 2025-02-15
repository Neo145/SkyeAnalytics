import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def load_data():
    """Load the cleaned WPL data"""
    try:
        current_dir = Path(__file__).parent
        data_path = current_dir.parent.parent / 'data' / 'processed' / 'wpl_clean.csv'
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def display_key_metrics(df):
    """Display key metrics in the dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Matches", len(df))
    
    with col2:
        win_by_runs = len(df[df['win_type'] == 'runs'])
        st.metric("Wins by Runs", win_by_runs)
    
    with col3:
        win_by_wickets = len(df[df['win_type'] == 'wickets'])
        st.metric("Wins by Wickets", win_by_wickets)
    
    with col4:
        toss_wins = len(df[df['won_toss_and_match']])
        toss_win_pct = (toss_wins / len(df)) * 100
        st.metric("Toss Winner Victory", f"{toss_win_pct:.1f}%")

def plot_team_performance(df):
    """Create team performance visualization"""
    st.subheader("Team Performance")
    
    # Calculate team statistics
    team_stats = []
    teams = set(df['team1'].unique()) | set(df['team2'].unique())
    
    for team in teams:
        matches_played = len(df[(df['team1'] == team) | (df['team2'] == team)])
        matches_won = len(df[df['winner'] == team])
        win_rate = (matches_won / matches_played * 100) if matches_played > 0 else 0
        
        team_stats.append({
            'Team': team,
            'Matches Played': matches_played,
            'Matches Won': matches_won,
            'Win Rate': win_rate
        })
    
    team_df = pd.DataFrame(team_stats)
    
    # Create visualization
    fig = px.bar(team_df, x='Team', y=['Matches Played', 'Matches Won'],
                 barmode='group', title='Team Performance Overview')
    
    st.plotly_chart(fig, use_container_width=True)

def plot_match_outcomes(df):
    """Create match outcomes visualization"""
    st.subheader("Match Outcomes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Win type pie chart
        win_type_counts = df['win_type'].value_counts()
        fig1 = px.pie(values=win_type_counts.values, 
                      names=win_type_counts.index,
                      title='Distribution of Win Types')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Venue distribution
        venue_counts = df['venue'].value_counts()
        fig2 = px.bar(x=venue_counts.index, y=venue_counts.values,
                      title='Matches per Venue')
        st.plotly_chart(fig2, use_container_width=True)

def show_wpl_dashboard():
    """Main function to display WPL dashboard"""
    st.title("Women's Premier League 2025 Analytics")
    
    # Load data
    df = load_data()
    
    if df is not None:
        # Add filters in expander
        with st.expander("📊 Filters and Controls", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                # Date range filter
                min_date = df['date'].min().date()
                max_date = df['date'].max().date()
                
                start_date = st.date_input(
                    "Start Date",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date
                )
            
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date
                )
            
            # Team filter
            teams = sorted(list(set(df['team1'].unique()) | set(df['team2'].unique())))
            selected_team = st.selectbox("Select Team", ['All Teams'] + teams)
        
        # Filter data based on selections
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        if selected_team != 'All Teams':
            mask = mask & ((df['team1'] == selected_team) | (df['team2'] == selected_team))
        
        filtered_df = df[mask].copy()
        
        if len(filtered_df) > 0:
            # Display visualizations
            display_key_metrics(filtered_df)
            plot_team_performance(filtered_df)
            plot_match_outcomes(filtered_df)
            
            # Match details table
            st.subheader("Match Details")
            st.dataframe(
                filtered_df[['date', 'team1', 'team2', 'winner', 'match_result', 'venue']].sort_values('date'),
                use_container_width=True
            )
        else:
            st.warning("No matches found for the selected filters.")