
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("🇲🇲 Myanmar Scenario Simulator (Monte Carlo)")

st.markdown("""
Simulate political and humanitarian outcomes in Myanmar based on regional and international actor behavior.  
Adjust probabilities below and click **Run Simulation** to generate scenario predictions.
""")

# Sidebar inputs
st.sidebar.header("Set Probabilities (%)")

def get_probs(options, label):
    with st.sidebar:
        total = 0
        probs = {}
        for opt in options:
            val = st.slider(f"{label} - {opt}", 0, 100, 0)
            probs[opt] = val
            total += val
        if total == 0:
            st.error(f"⚠️ Total probability for {label} is 0. Please adjust.")
        elif total != 100:
            st.warning(f"⚠️ Total for {label} = {total}%. Should be 100%.")
        return {k: v/100 for k, v in probs.items()} if total == 100 else None

china_probs = get_probs(["Supports SAC", "Neutral", "Pressures for Reform"], "China")
eaos_probs = get_probs(["Fragmented", "Unified"], "EAOs")
india_probs = get_probs(["Engaged", "Passive"], "India")
bangladesh_probs = get_probs(["Seeks Repatriation", "Neutral"], "Bangladesh")
russia_probs = get_probs(["Arms Support", "Neutral"], "Russia")
usa_probs = get_probs(["Active Diplomacy", "Gradual Disengagement"], "USA")

run = st.button("🚀 Run Simulation")

if run and all([china_probs, eaos_probs, india_probs, bangladesh_probs, russia_probs, usa_probs]):
    def weighted_choice(prob_dict):
        options = list(prob_dict.keys())
        weights = list(prob_dict.values())
        return np.random.choice(options, p=weights)

    n = 10000
    simulations = []
    for _ in range(n):
        sim = {
            "China": weighted_choice(china_probs),
            "EAOs": weighted_choice(eaos_probs),
            "India": weighted_choice(india_probs),
            "Bangladesh": weighted_choice(bangladesh_probs),
            "Russia": weighted_choice(russia_probs),
            "USA": weighted_choice(usa_probs)
        }

        if (sim["China"] == "Supports SAC" and sim["EAOs"] == "Fragmented" and 
            sim["USA"] == "Gradual Disengagement" and sim["Russia"] == "Arms Support"):
            outcome = "Prolonged Conflict"
            impact = "High Humanitarian Needs"
        elif (sim["China"] == "Pressures for Reform" and sim["EAOs"] == "Unified" and 
              sim["USA"] == "Active Diplomacy"):
            outcome = "Fragile Negotiation"
            impact = "Moderate Humanitarian Needs"
        elif (sim["China"] == "Neutral" and sim["EAOs"] == "Unified" and 
              sim["India"] == "Engaged" and sim["Bangladesh"] == "Seeks Repatriation"):
            outcome = "Political Transition"
            impact = "Managed Humanitarian Situation"
        elif (sim["Bangladesh"] == "Seeks Repatriation" and sim["EAOs"] == "Fragmented" and 
              sim["Russia"] == "Arms Support" and sim["USA"] == "Gradual Disengagement"):
            outcome = "State Collapse / Partition"
            impact = "Severe Humanitarian Crisis"
        else:
            outcome = "Status Quo / Frozen Conflict"
            impact = "Ongoing Humanitarian Needs"

        sim["Outcome"] = outcome
        sim["Humanitarian Impact"] = impact
        simulations.append(sim)

    df = pd.DataFrame(simulations)
    st.success("✅ Simulation completed!")

    # Outcome plot
    st.subheader("📊 Scenario Outcomes")
    outcome_counts = df["Outcome"].value_counts(normalize=True) * 100
    st.bar_chart(outcome_counts)

    # Impact plot
    st.subheader("🚨 Humanitarian Impact")
    impact_counts = df["Humanitarian Impact"].value_counts(normalize=True) * 100
    st.bar_chart(impact_counts)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Raw Data (CSV)", data=csv, file_name="myanmar_simulation.csv")
