import streamlit as st

st.title("Alô mundo!🪩")
st.header("Bem-vindo ao site mais novo da Nanda!💖")
st.write("Só preencha abaixo com algumas informaçõezinhas paa conhecê-lo melhor.😁")

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.write(f"Olá, {nome}! Seja bem-vindo(a) ao meu app!😊")
