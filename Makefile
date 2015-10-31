include $(AMBERHOME)/AmberTools/src/config.h

install:
	$(PYTHON) setup.py install --prefix=$(AMBERHOME) --install-scripts=$(BINDIR)

clean:
	/bin/rm -rf build/

uninstall:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/OptC4.py $(BINDIR)/PdbSearcher.py ${BINDIR}/espgen.py ${BINDIR}/CartHess2FC.py

test:
	/bin/rm -rf $(AMBERHOME)/AmberTools/test/pymsmt/mcpb
	cp -r $(AMBERHOME)/AmberTools/src/pymsmt/tests/gaussian/ $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/ ; \
     cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb ; ./Run.pymsmt
	/bin/rm -rf $(AMBERHOME)/AmberTools/test/pymsmt/mcpb
	cp -r $(AMBERHOME)/AmberTools/src/pymsmt/tests/gamess/ $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/ ; \
     cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb ; ./Run.pymsmt

skip:
	@echo ""
	@echo "Skipping installation of pyMSMT."
	@echo ""

