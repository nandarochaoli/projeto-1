import streamlit as st

st.title("Alô mundo! 🪩")
st.header("Bem-vindo ao site mais novo da Nanda! 💖")
st.write("Só preencha abaixo com algumas informaçõezinhas para conhecê-lo melhor. 😁")

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.write(f"Olá, {nome}! Fico muito feliz por você estar aqui! 😊")

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


st.title("😄 Como você está hoje?")

humor = st.selectbox("Escolha seu humor:", ["Feliz", "Cansado", "Animado", "Estressado"])

st.write(f"Você está {humor} hoje")

if humor == "Feliz":
    st.write("Maravilha! Aproveite e vá fazer o que mais gosta!")
    
elif humor == "Cansado":
    st.write("Entendo...tente descansar ao ar livre, costuma me ajudar!")
    
elif humor == "Animado":
    st.write("Ótimo, tenha um dia perfeto!")
    
elif humor == ("Estressado"):
    st.write("Todos temos esses dias... se aproxime das pessoas que ama, tenho certeza que será relaxante.") 
    
