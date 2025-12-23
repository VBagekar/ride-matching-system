import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Ride Matching System", layout="centered")

st.title("🚗 Ride Matching System")

menu = st.sidebar.selectbox(
    "Choose Role",
    ["Rider", "Driver"]
)

# ---------------- RIDER UI ----------------
if menu == "Rider":
    st.header("👤 Rider")

    name = st.text_input("Name")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")

    if st.button("Register Rider"):
        res = requests.post(
            f"{BASE_URL}/riders/",
            json={"name": name, "latitude": lat, "longitude": lon}
        )
        if res.status_code == 200:
            st.success(f"Rider registered with ID: {res.json()['id']}")
        else:
            st.error(res.text)

    st.divider()
    rider_id = st.number_input("Rider ID", step=1)

    if st.button("Request Ride"):
        res = requests.post(
            f"{BASE_URL}/rides/request",
            json={"rider_id": int(rider_id)}
        )
        if res.status_code == 200:
            ride = res.json()
            st.success("Ride Requested!")
            st.json(ride)
        else:
            st.error(res.text)

# ---------------- DRIVER UI ----------------
if menu == "Driver":
    st.header("🚕 Driver")

    name = st.text_input("Name")
    lat = st.number_input("Latitude", format="%.6f", key="dlat")
    lon = st.number_input("Longitude", format="%.6f", key="dlon")

    if st.button("Register Driver"):
        res = requests.post(
            f"{BASE_URL}/drivers/",
            json={"name": name, "latitude": lat, "longitude": lon}
        )
        if res.status_code == 200:
            st.success(f"Driver registered with ID: {res.json()['id']}")
        else:
            st.error(res.text)

    st.divider()
    ride_id = st.number_input("Ride ID", step=1)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Accept Ride"):
            res = requests.post(f"{BASE_URL}/rides/{int(ride_id)}/accept")
            st.json(res.json())

    with col2:
        if st.button("Complete Ride"):
            res = requests.post(f"{BASE_URL}/rides/{int(ride_id)}/complete")
            st.json(res.json())
