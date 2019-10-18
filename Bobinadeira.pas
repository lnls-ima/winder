unit Bobinadeira;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Menus, ExtCtrls, Loco3, Buttons;

type
  TFBobinadeira = class(TForm)
    Image1: TImage;
    ERazaoM1: TEdit;
    ERazaoM2: TEdit;
    RSDriver: TRs232;
    ENVoltas: TEdit; //
    Contador: TLabel; //
    GBMove: TGroupBox;
    SBneg: TSpeedButton; //
    SBpos: TSpeedButton; //
    GBConfDriver: TGroupBox;
    Label2: TLabel;
    EVelM: TEdit; //
    Label1: TLabel;
    Label3: TLabel;
    EAceM: TEdit; //
    Label4: TLabel;
    Label5: TLabel;
    BBConfiguraDriver: TBitBtn; //
    procedure FormShow(Sender: TObject);
    procedure ConfiguraDrivers;
    procedure ENVoltasDblClick(Sender: TObject);
    procedure ERazaoM1Exit(Sender: TObject);
    procedure ERazaoM2Exit(Sender: TObject);
    procedure EVelMExit(Sender: TObject);
    procedure EAceMExit(Sender: TObject);
    procedure BBConfiguraDriverClick(Sender: TObject);
    procedure SBposMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure SBposMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure SBnegMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure SBnegMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure LerPosicao;
    procedure FormClose(Sender: TObject; var Action: TCloseAction);

  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  FBobinadeira: TFBobinadeira;

  VelM1       : double;
  VelM2       : double;
  AceM1       : double;
  AceM2       : double;

  Razao       : double;

  NVolta      : double;
const
  CRLF       = #13+#10;
  VoltaMotor = 25000;

implementation

{$R *.DFM}

procedure TFBobinadeira.FormShow(Sender: TObject);
begin
   Abreloco;
   RSDriver.Abre;
   RSDriver.BaudRate := 9600;
   RSDriver.DataBits := 8;
   RSDriver.StopBits := Dois;
   RSDriver.Paridade := Nenhuma;

   ConfiguraDrivers;
   GBMove.Enabled := True;
end;

procedure TFBobinadeira.ConfiguraDrivers;
begin
   Razao := StrToFloat(ERazaoM2.Text);

   VelM1 := StrToFloat(EVelM.Text);
   AceM1 := StrToFloat(EAceM.Text);

   VelM2 := StrToFloat(EVelM.Text)*Razao;
   AceM2 := StrToFloat(EAceM.Text)*Razao;

   {Motor 1}
   RSDriver.Escrita('1LD3'+CRLF); //LIMIT DISABLE
   RSDriver.Escrita('1MC'+CRLF); //MODE CONTINUOUS (JOG)
   RSDriver.Escrita('1V'+FloatToStr(VelM1)+CRLF);
   RSDriver.Escrita('1A'+FloatToStr(AceM1)+CRLF);

   {Motor 2}
   RSDriver.Escrita('2LD3'+CRLF);
   RSDriver.Escrita('2MC'+CRLF);
   RSDriver.Escrita('2V'+FloatToStr(VelM2)+CRLF);
   RSDriver.Escrita('2A'+FloatToStr(AceM2)+CRLF);
end;

procedure TFBobinadeira.ENVoltasDblClick(Sender: TObject);
var
InputString : string;
begin
   InputString:= InputBox('Zerar contador de voltas', 'Digite a senha correta para zerar o contador!', '');

   if InputString = 'potye' then
   begin
      ENVoltas.Text := '0.0';
      RSDriver.Escrita ('1PZ'+CRLF); //Set Abs Counter to zero
      RSDriver.Escrita ('2PZ'+CRLF);
   end
   else
      MessageDlg('Senha incorreta!!!', mtInformation,[mbOk], 0);
end;

procedure TFBobinadeira.ERazaoM1Exit(Sender: TObject);
begin
   ERazaoM1.Text := FloatToStrF((StrToFloat(ERazaoM1.Text)),ffFixed,10,2);
   ERazaoM2.Text := FloatToStrF((StrToFloat(ERazaoM1.Text)*0.04),ffFixed,10,2);
end;

procedure TFBobinadeira.ERazaoM2Exit(Sender: TObject);
begin
   if (ERazaoM2.Text = '') then
   begin
      MessageDlg('Configure a razao entre os motores corretamente!', mtInformation,[mbOk], 0);
      exit;
   end;

   ERazaoM2.Text := FloatToStrF((StrToFloat(ERazaoM2.Text)),ffFixed,10,3);
   GBMove.Enabled := False;
end;

procedure TFBobinadeira.EVelMExit(Sender: TObject);
begin
   if (EVelM.Text = '') then
   begin
      MessageDlg('Configure a velocidade e aceleração corretamente!', mtInformation,[mbOk], 0);
      exit;
   end;

   if StrToFloat(EVelM.Text) > 2 then
   begin
      MessageDlg('O limite de velocidade é de 2 rev/s!', mtInformation,[mbOk], 0);
      EVelM.Text := '2.000';
   end;

   EVelM.Text := FloatToStrF((StrToFloat(EVelM.Text)),ffFixed,10,3);
   GBMove.Enabled := False;
end;

procedure TFBobinadeira.EAceMExit(Sender: TObject);
begin
   if (EAceM.Text = '') then
   begin
      MessageDlg('Configure a velocidade e aceleração corretamente!', mtInformation,[mbOk], 0);
      exit;
   end;
   
   EAceM.Text := FloatToStrF((StrToFloat(EAceM.Text)),ffFixed,10,3);
   GBMove.Enabled := False;
end;

procedure TFBobinadeira.BBConfiguraDriverClick(Sender: TObject);
begin
   if (EVelM.Text = '') or (EAceM.Text = '') then
   begin
      MessageDlg('Configure a velocidade e aceleração corretamente!', mtInformation,[mbOk], 0);
      exit;
   end;

   ConfiguraDrivers;

   MessageDlg('Configuração realizada'+CRLF+'Razão entre motores: 1 para '+FloatToStrF(Razao,ffFixed,10,3), mtInformation,[mbOk], 0);

   GBMove.Enabled := True;
end;

procedure TFBobinadeira.SBposMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
begin
   RsDriver.Escrita('1H+'+CRLF); //Direcao positiva
   RsDriver.Escrita('2H+'+CRLF);

   RSDriver.Escrita('1G'+CRLF);
   RSDriver.Escrita('2G'+CRLF);
end;

procedure TFBobinadeira.SBposMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
   RsDriver.Escrita('1S'+CRLF); //Stop
   RsDriver.Escrita('2S'+CRLF);
   LerPosicao;
end;

procedure TFBobinadeira.SBnegMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
begin
   RsDriver.Escrita('1H-'+CRLF);
   RsDriver.Escrita('2H-'+CRLF);

   RSDriver.Escrita('1G'+CRLF);
   RSDriver.Escrita('2G'+CRLF);
end;

procedure TFBobinadeira.SBnegMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
   RsDriver.Escrita('1S'+CRLF);
   RsDriver.Escrita('2S'+CRLF);
   LerPosicao;
end;

procedure TFBobinadeira.LerPosicao;
var
aux: string;
i : integer;
begin
   repeat
      Application.ProcessMessages;
      RSDriver.LimpaTX;
      RSDriver.LimpaRX;
      RSDriver.Escrita('1R'+CRLF); //Request index status
      aux := RSDriver.Leitura(5);
      i := Pos('*R', aux);
   until(i <> 0);

   RSDriver.LimpaTX;
   RSDriver.LimpaRX;
   RSDriver.Escrita('1PR'+CRLF); //Abs position report
   aux := RSDriver.Leitura(20);
   i := Pos('*', aux);
   aux := Copy(aux,i+1,length(aux));
   i := Pos(#13, aux);
   aux := Copy(aux,1,i-1);
   NVolta := StrToFloat(aux)/VoltaMotor;

   ENVoltas.Text := FloatToStrF(NVolta,ffFixed,10,1);
end;

procedure TFBobinadeira.FormClose(Sender: TObject;
  var Action: TCloseAction);
begin
   RSDriver.Fecha;
end;

end.

