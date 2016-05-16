include ../config.h

install:
	$(PYTHON) setup.py install --prefix=$(AMBERHOME) --install-scripts=$(BINDIR)

install14:
	./setup.sh $(BINDIR) $(PYTHON)

install15: install
install16: install

clean:
	/bin/rm -rf build/

uninstall:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/PdbSearcher.py $(BINDIR)/CartHess2FC.py $(BINDIR)/espgen.py

uninstall14:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/PdbSearcher.py $(BINDIR)/CartHess2FC.py $(BINDIR)/espgen.py \
    /bin/rm -rf $(BINDIR)/api $(BINDIR)/mcpb $(BINDIR)/lib $(BINDIR)/msmtmol $(BINDIR)/ipmach $(BINDIR)/pymsmtexp.py $(BINDIR)/title.py

uninstall15: uninstall
uninstall16: uninstall

test:
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03 ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g03/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03 ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09 ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g09/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09 ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/gms/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms ; ./Run.pymsmt

skip:
	@echo ""
	@echo "Skipping installation of pyMSMT."
	@echo ""

