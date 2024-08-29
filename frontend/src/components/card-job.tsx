import { FormModalContext } from "../context/form-modal-context";
import { Ellipsis, Pencil, Trash2 } from "lucide-react";
import { useState, useContext } from "react";
import logo from "../assets/img/logo.svg";
import "../css/card-job.css";

export const CardJob: React.FC = () => {
  // lida com modal de ações (editar/deletar) no mobile
  const [showActions, setShowActions] = useState<boolean>(false);

  const context = useContext(FormModalContext);
  if (!context) {
    throw new Error();
  }
  const { handleEditModal } = context;

  const handleEditButtonClick = () => {
    handleEditModal();
    setShowActions(false);
  };

  return (
    <div className="card__content">
      <Ellipsis
        size={28}
        className="ellipsis-button"
        onClick={() => setShowActions(!showActions)}
      />
      <div className="card__content--img">
        <img src={logo} alt="Imagem" />
      </div>
      <div className="card__content--info">
        <p className="card__content--title">Desenvolvedor Python</p>
        <p className="card__content--description">
          Desenvolvimento de aplicações web utilizando Python e Django.
        </p>
        <p className="card__content--date">22/08/2024</p>
      </div>

      <div
        className={`modal-overlay ${showActions ? "visible" : ""}`}
        onClick={() => setShowActions(!showActions)}
      ></div>

      <div
        className={`card__content--actions ${showActions ? "visible" : ""}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-actions--btns">
          <Pencil className="update-button" onClick={handleEditButtonClick} />
          <Trash2 className="delete-button" />
        </div>
      </div>
    </div>
  );
};
