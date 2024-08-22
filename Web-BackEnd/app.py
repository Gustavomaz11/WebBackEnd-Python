from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conexao = pymysql.connect(
    #Aqui deve ser colocado as informações do banco de dados
    host='',
    user='',
    password='',
    database=''
)

conexao.connect()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome_mae = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        nome_mae = request.form.get('nome-mae')

        new_user = User(
            nome=nome,
            idade=idade,
            email=email,
            cpf=cpf,
            nome_mae=nome_mae
        )

        conexao.begin()

        cur = conexao.cursor()

        sql = """insert into tbRegistro (ID,nome,idade,email,cpf,mae) VALUES (%s,%s,%s,%s,%s,%s)"""

        cur.execute(sql,(3,nome,idade,email,cpf,nome_mae))

        conexao.commit()


        return redirect(url_for('index'))


    form_html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Formulário de Inscrição</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                font-family: Arial, Helvetica, sans-serif;
            }

            body {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding-top: 8%;
                background-color: #f2f2f2;
            }

            h1 {
                margin-bottom: 1rem;
            }

            form {
                display: flex;
                flex-direction: column;
                width: 25%;
                border: 1px solid #000;
                padding: 20px;
                border-radius: 5px;
                background-color: #f2f2f2;
            }

            input {
                padding: 10px;
                border-radius: 2rem;
                border: none;

            }

            form label {
                margin-bottom: 0.5rem;
            }

            button {
                padding: 10px;
                border-radius: 2rem;
                border: none;
                background-color: #000;
                color: #fff;
                cursor: pointer;
                transition: 0.6s;
            }

            button:hover {
                background-color: grey;
            }
        </style>
    </head>
    <body>
        <h1>Formulário de Inscrição</h1>
        <form method="POST" action="/">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" placeholder="Digite o seu nome..." required><br><br>

            <label for="idade">Idade:</label>
            <input type="number" id="idade" name="idade" placeholder="Digite a sua idade..." required><br><br>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Digite o seu e-mail" required><br><br>

            <label for="cpf">CPF:</label>
            <input type="text" id="cpf" name="cpf" placeholder="Digite o seu CPF..." required><br><br>

            <label for="nome-mae">Nome da Mãe:</label>
            <input type="text" id="nome-mae" name="nome-mae" placeholder="Digite o nome da sua mãe..." required><br><br>

            <button type="submit">Cadastrar</button>
        </form>
    </body>
    </html>
    '''

   
    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(debug=True)
