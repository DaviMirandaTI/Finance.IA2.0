import { useState } from "react";
import bcrypt from "bcryptjs";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";
import { LogIn, UserPlus, Wallet } from "lucide-react";

export function LoginView({ users, setUsers, setIsLoggedIn, setCurrentUser }) {
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    
    const user = users.find(u => u.email === loginEmail);
    if (!user) {
      toast.error("Usuário não encontrado!");
      return;
    }

    const isValid = await bcrypt.compare(loginPassword, user.passwordHash);
    if (!isValid) {
      toast.error("Senha incorreta!");
      return;
    }

    const sessionUser = {
      userId: user.id,
      name: user.name,
      email: user.email,
      isLoggedIn: true
    };

    setCurrentUser(sessionUser);
    setIsLoggedIn(true);
    toast.success(`Bem-vindo, ${user.name}!`);
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (users.some(u => u.email === registerEmail)) {
      toast.error("E-mail já cadastrado!");
      return;
    }

    const passwordHash = await bcrypt.hash(registerPassword, 10);
    const newUser = {
      id: crypto.randomUUID(),
      name: registerName,
      email: registerEmail,
      passwordHash,
      createdAt: new Date().toISOString()
    };

    setUsers(prev => [...prev, newUser]);
    
    const sessionUser = {
      userId: newUser.id,
      name: newUser.name,
      email: newUser.email,
      isLoggedIn: true
    };

    setCurrentUser(sessionUser);
    setIsLoggedIn(true);
    toast.success("Conta criada com sucesso!");
  };

  return (
    <div className="login-container">
      <div className="login-wrapper">
        <div className="login-header">
          <Wallet className="login-logo" size={48} />
          <h1 className="login-title">FinSystem v2.0</h1>
          <p className="login-subtitle">Seu controle financeiro completo</p>
        </div>

        <Tabs defaultValue="login" className="login-tabs">
          <TabsList className="login-tabs-list">
            <TabsTrigger value="login" className="login-tab">
              <LogIn size={16} />
              <span>Login</span>
            </TabsTrigger>
            <TabsTrigger value="register" className="login-tab">
              <UserPlus size={16} />
              <span>Criar Conta</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <Card className="login-card">
              <CardHeader>
                <CardTitle>Entrar na sua conta</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleLogin} className="login-form">
                  <div>
                    <Label>E-mail</Label>
                    <Input 
                      type="email" 
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                      placeholder="seu@email.com"
                      required
                      data-testid="login-email-input"
                    />
                  </div>
                  <div>
                    <Label>Senha</Label>
                    <Input 
                      type="password" 
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      placeholder="••••••••"
                      required
                      data-testid="login-password-input"
                    />
                  </div>
                  <Button type="submit" className="w-full" data-testid="login-submit-btn">
                    <LogIn size={16} />
                    <span>Entrar</span>
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="register">
            <Card className="login-card">
              <CardHeader>
                <CardTitle>Criar nova conta</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleRegister} className="login-form">
                  <div>
                    <Label>Nome completo</Label>
                    <Input 
                      type="text" 
                      value={registerName}
                      onChange={(e) => setRegisterName(e.target.value)}
                      placeholder="Seu nome"
                      required
                      data-testid="register-name-input"
                    />
                  </div>
                  <div>
                    <Label>E-mail</Label>
                    <Input 
                      type="email" 
                      value={registerEmail}
                      onChange={(e) => setRegisterEmail(e.target.value)}
                      placeholder="seu@email.com"
                      required
                      data-testid="register-email-input"
                    />
                  </div>
                  <div>
                    <Label>Senha</Label>
                    <Input 
                      type="password" 
                      value={registerPassword}
                      onChange={(e) => setRegisterPassword(e.target.value)}
                      placeholder="Mínimo 6 caracteres"
                      minLength={6}
                      required
                      data-testid="register-password-input"
                    />
                  </div>
                  <Button type="submit" className="w-full" data-testid="register-submit-btn">
                    <UserPlus size={16} />
                    <span>Criar conta</span>
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
