import streamlit as st

st.title("Alô mundo! 🪩")
st.header("Bem-vindo ao site mais novo da Nanda! 💖")
st.write("Só preencha abaixo com algumas informaçõezinhas paa conhecê-lo melhor. 😁")

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.write(f"Olá, {nome}! Seja bem-vindo(a) ao meu app! 😊")

st.title("Calculadora simples 🧮")
st.header("Instruções:")
st.write(f"{nome}, digite dois algarismos nas lacunas abaixo e clique nos botões das operações matemáticas desejadas.")

a = st.number_input("Digite o primeiro número:")
b = st.number_input("Digite o segundo número:")

if st.button("Somar"):
    st.write("Resultado:", a + b)

if st.button("Subtrair"):
    st.write("Resultado", a - b)

if st.button("Multiplicar"):
    st.write("Resultado", a * b)

if st.button("Dividir"):
    st.write("Resultado", a / b)

