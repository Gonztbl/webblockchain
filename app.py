from flask import Flask, render_template, url_for, redirect, abort, request, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from web3 import Web3
import json

# =========================================================== WEB3 ======================================================================
network_url = "HTTP://127.0.0.1:8545"
web = Web3(Web3.HTTPProvider(network_url))

with open('./build/contracts/Election.sol/Election.json', 'r', encoding='utf-8') as f:
    hardhatFile = json.load(f)
abi = hardhatFile['abi']


# Tạo hợp đồng
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Thay bằng địa chỉ contract nếu đã deploy
if contract_address:
    election = web.eth.contract(address=contract_address, abi=abi)
else:
    election = None
    print("Contract not deployed or invalid contract address")

end = False  # Trạng thái kết thúc bầu cử

# =========================================================== FLASK CONFIG ======================================================================
app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SECRET_KEY'] = 'THIS_IS_A_SECRET_KEY'

# =========================================================== USER CLASS ======================================================================
class User(UserMixin):
    def __init__(self, username, password, address, key):
        self.username = username
        self.password = password
        self.address = address
        self.key = key

    def get_id(self):
        return self.username

# Tạo danh sách người dùng cố định
users = [
    User(
        username="admin",
        password=bcrypt.generate_password_hash("adminpassword").decode("utf-8"),
        address="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        key="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
    ),
    User(
        username="user1",
        password=bcrypt.generate_password_hash("userpassword1").decode("utf-8"),
        address="0x70997970C51812dc3A010C7d01b50e0d17dc79C8",  # Địa chỉ ví của người dùng, thay bằng địa chỉ hợp lệ
        key="0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",  # Khóa riêng của người dùng, thay bằng khóa hợp lệ
    ),
    User(
        username="user2",
        password=bcrypt.generate_password_hash("userpassword2").decode("utf-8"),
        address="0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",  # Địa chỉ ví của người dùng, thay bằng địa chỉ hợp lệ
        key="0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",  # Khóa riêng của người dùng, thay bằng khóa hợp lệ
    ),
]

@login_manager.user_loader
def load_user(username):
    return next((user for user in users if user.username == username), None)

# =========================================================== FORMS ======================================================================
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Address"})
    key = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Key"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        if any(user.username == username.data for user in users):
            raise ValidationError("Username already exists. Please choose another.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In")

# =========================================================== ROUTES ======================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((u for u in users if u.username == form.username.data), None)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['has_voted'] = False
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            address=form.address.data,
            key=form.key.data
        )
        users.append(new_user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('has_voted', None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((u for u in users if u.username == form.username.data), None)
        if user and user.username == "admin" and bcrypt.check_password_hash(user.password, "adminpassword"):
            login_user(user)
            return redirect(url_for('adminPortal'))
        else:
            abort(403)
    return render_template('adminLogin.html', form=form)

# Sửa từ 1, 2, 3 thành 0, 1, 2
@app.route('/adminPortal', methods=['GET', 'POST'])
@login_required
def adminPortal():
    if current_user.username != "admin":
        abort(403)
    # SỬA Ở ĐÂY
    candidate1 = election.functions.candidates(0).call()
    candidate2 = election.functions.candidates(1).call()
    candidate3 = election.functions.candidates(2).call()
    # Không cần thay đổi các dòng bên dưới
    print(candidate1)
    print(candidate2)
    print(candidate3)
    candidates = [candidate1, candidate2, candidate3]
    return render_template('admin.html', candidates=candidates)


@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if session.get('has_voted', False):
        return "<h1>You have already voted in this session.</h1>"

    if end:
        return "<h1>ELECTION ENDED</h1>"
    # Sửa lại toàn bộ hàm này

    # Sửa lại toàn bộ hàm này
    def cast_vote(owner, signature, to_vote):
        if not election:
            return None
        try:
            # 1. Lấy nonce (số thứ tự giao dịch)
            nonce = web.eth.get_transaction_count(owner)
            
            # 2. Lấy chainId của mạng
            chain_id = web.eth.chain_id

            # 3. Chuẩn bị các thông tin cần thiết cho giao dịch
            # Xây dựng đối tượng giao dịch thô
            tx_params = {
                'from': owner,
                'nonce': nonce,
                
                'gas': 500000, # Ước tính một lượng gas an toàn
                'gasPrice': web.to_wei('10', 'gwei'),
                'chainId': chain_id,
                # 'value' có thể bỏ qua vì đây không phải giao dịch chuyển ETH
            }

            # 4. Xây dựng giao dịch bằng cách gọi hàm của hợp đồng
            # .build_transaction() sẽ điền 'data' vào tx_params
            unsigned_transaction = election.functions.vote(to_vote).build_transaction(tx_params)

            # 5. Ký giao dịch bằng khóa riêng tư
            signed_transaction = web.eth.account.sign_transaction(unsigned_transaction, private_key=signature)

            # 6. Gửi giao dịch đã ký lên blockchain
            tx_hash = web.eth.send_raw_transaction(signed_transaction.rawTransaction)

            # 7. (Tùy chọn nhưng rất khuyến khích) Chờ giao dịch được xác nhận
            tx_receipt = web.eth.wait_for_transaction_receipt(tx_hash)

            print(f"Vote cast successfully! Transaction receipt: {tx_receipt}")
            return tx_receipt # Trả về biên lai giao dịch nếu thành công

        except Exception as e:
            # In lỗi chi tiết hơn để gỡ lỗi
            print(f"Error casting vote for address {owner}: {e}")
            return None

    if request.method == 'POST':
        candidate = request.form.get('voteBtn')
        candidate_map = {'De 1': 0, 'De 2': 1, 'De 3': 2}
        to_vote = candidate_map.get(candidate)

        if to_vote is None:
            return "<h1>Invalid candidate selected.</h1>"
        print(current_user.address)
        result = cast_vote(current_user.address, current_user.key, to_vote)
        if result:
            session['has_voted'] = True
            return redirect(url_for('home'))
        return "<h1>Error casting your vote. Please try again later.</h1>"

    return render_template('vote.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
